#!/usr/bin/env python3
"""Static artifact validation. This is not browser or product acceptance testing."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DIST=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'dist'
CONFIG=json.loads((ROOT/'site.config.json').read_text())
DOMAIN=CONFIG['domain']
BASE=CONFIG.get('deployment_url', 'https://'+DOMAIN).rstrip('/')
errors=[]
counts={'html_pages':0,'local_references':0,'anchors':0,'sitemap_urls':0,'asset_hashes':0}

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs=[];self.ids=set();self.meta={};self.links={};self.h1=0;self.title='';self.in_title=False;self.lang=None;self.languages={};self.alternates={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='title':self.in_title=True
        if tag=='h1':self.h1+=1
        if 'id' in a:
            if a['id'] in self.ids:errors.append('Duplicate id: '+a['id'])
            self.ids.add(a['id'])
        if tag=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if tag=='link':self.links[a.get('rel','')]=a.get('href','')
        if tag=='link' and a.get('rel')=='alternate':self.alternates[a.get('hreflang')]=a.get('href')
        if a.get('data-language'):self.languages[a['data-language']]=(a.get('href'),a.get('aria-current'))
        if tag=='svg' and 'viewbox' not in a:errors.append('Inline SVG viewBox missing')
        for key in ('href','src','data-screen'):
            if key in a:self.refs.append((tag,key,a[key]))
        if tag=='img' and not a.get('alt') and a.get('aria-hidden')!='true':errors.append('Missing image alt text')
        if tag=='button' and a.get('type')!='button':errors.append('Button has no explicit type')
        if tag in ('iframe','form'):errors.append('Unexpected active form/frame')
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
    def handle_data(self,text):
        if self.in_title:self.title+=text

pages={}
for f in sorted(DIST.rglob('*.html')):
    p=Page();p.feed(f.read_text());pages[f]=p;counts['html_pages']+=1
    if p.h1!=1:errors.append(f'{f.relative_to(DIST)}: expected exactly one h1')
    chinese=f.relative_to(DIST).parts[0]=='zh'
    if p.lang!=('zh-CN' if chinese else 'en'):errors.append(f'{f.name}: lang missing')
    if not p.title or len(p.meta.get('description',''))<(15 if chinese else 30):errors.append(f'{f.name}: missing title/description')
    for prop in ('og:title','og:description','og:image','og:url','robots'):
        if not p.meta.get(prop):errors.append(f'{f.name}: missing {prop}')
    expected=BASE+('/' if f==DIST/'index.html' else '/'+f.relative_to(DIST).as_posix().replace('index.html',''))
    if p.links.get('canonical')!=expected or p.meta.get('og:url')!=expected:errors.append(f'{f.name}: canonical/OG mismatch')
    if not CONFIG.get('public_release') and p.meta.get('robots')!='noindex,follow':errors.append('Preview indexing enabled')
    if p.meta.get('og:image')!=BASE+'/assets/og/norm-preview.png':errors.append('OG image mismatch')
    logical=f.relative_to(DIST).as_posix().removeprefix('zh/')
    for lang,prefix in [('en',''),('zh-CN','zh/'),('x-default','')]:
        if p.alternates.get(lang)!=BASE+'/'+prefix+logical.replace('index.html',''):errors.append(f'{f}: invalid hreflang {lang}')
    if logical!='404.html':
        for lang,prefix in [('en',''),('zh','zh/')]:
            href,current=p.languages.get(lang,('',None))
            if not href or (f.parent/href).resolve()!=DIST/prefix/logical:errors.append(f'{f}: language switch does not preserve route')
            if (current=='true')!=(lang==('zh' if chinese else 'en')):errors.append(f'{f}: wrong current language')

titles=[p.title for p in pages.values()]
if len(titles)!=len(set(titles)):errors.append('Duplicate page titles')
descs=[p.meta['description'] for p in pages.values()]
if len(descs)!=len(set(descs)):errors.append('Duplicate page descriptions')
for f,p in pages.items():
    for tag,key,ref in p.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:
            if key=='src':errors.append('External runtime asset: '+ref)
            if u.scheme=='mailto' and not (CONFIG.get('contact_enabled') and CONFIG.get('email_destination_verified') and CONFIG.get('email_routing_enabled')):errors.append('Contact not configured')
            if u.scheme=='mailto' and u.path!=CONFIG['email']:errors.append('Unexpected contact address')
            continue
        if u.path.startswith('/'):errors.append(f'{f.name}: offline-incompatible absolute path {ref}')
        if not u.path:target=f
        else:
            target=(f.parent/unquote(u.path)).resolve()
            if target.is_dir():errors.append(f'{f.name}: directory link lacks index.html: {ref}')
        if not target.is_relative_to(DIST):errors.append('Reference escapes dist: '+ref)
        elif not target.is_file():errors.append(f'{f.relative_to(DIST)}: missing target {ref}')
        else:counts['local_references']+=1
        if u.fragment:
            counts['anchors']+=1
            if target in pages and unquote(u.fragment) not in pages[target].ids:errors.append('Broken anchor '+ref)

for f in DIST.rglob('*.css'):
    text=f.read_text()
    for ref in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)',text):
        if ref.startswith('data:'):continue
        if '://' in ref:errors.append('External CSS asset: '+ref)
        elif not (f.parent/ref).is_file():errors.append('Missing CSS asset: '+ref)
    if text.count('{')!=text.count('}'):errors.append('Unbalanced CSS braces')
for f in DIST.rglob('*.svg'):
    try:ET.parse(f)
    except ET.ParseError as e:errors.append(f'{f.name}: malformed SVG: {e}')

ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
for loc in ET.parse(DIST/'sitemap.xml').findall('.//s:loc',ns):
    u=urlsplit(loc.text)
    site_path=urlsplit(BASE).path.rstrip('/')+'/'
    relative_path=u.path.removeprefix(site_path)
    target=DIST/relative_path
    if u.path.endswith('/'):target=target/'index.html'
    if u.netloc!=urlsplit(BASE).netloc or not u.path.startswith(site_path) or target not in pages:errors.append('Invalid sitemap URL '+loc.text)
    counts['sitemap_urls']+=1

manifest=json.loads((DIST/'BUILD_MANIFEST.json').read_text())
for name,sha in manifest['files'].items():
    f=DIST/name
    if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=sha:errors.append('Manifest hash mismatch '+name)
    counts['asset_hashes']+=1

for f in DIST.rglob('*'):
    if not f.is_file():continue
    if f.suffix.lower() in ('.woff','.woff2','.ttf','.otf','.zip','.pdf','.md','.py'):errors.append('Unexpected public file '+f.name)
    if f.suffix in ('.html','.css','.js','.json','.svg','.txt','.xml'):
        text=f.read_text()
        for bad in ['UFORCE','uforce.com','localhost','127.0.0.1','D:\\','/workspace/','/root/','candidate-12','CP42','ghp_','github_pat_','sk-proj-','cfat_']:
            if bad in text:errors.append(f'{f.name}: prohibited private/reference string {bad}')
        if re.search(r'(?:api[_-]?key|authorization)\s*[:=]\s*[\"\'][A-Za-z0-9_-]{18,}',text,re.I):errors.append('Possible secret: '+f.name)
        if f.suffix=='.js' and re.search(r'\b(fetch|XMLHttpRequest|WebSocket|localStorage|sessionStorage)\b',text):errors.append('Unexpected network/storage behavior')

if not (DIST/'assets/og/norm-preview.png').is_file():errors.append('Missing OG raster')
if (DIST/'CNAME').read_text().strip()!=DOMAIN:errors.append('CNAME mismatch')
if counts['html_pages']!=26 or counts['sitemap_urls']!=24:errors.append('Incorrect page count')
result={'scope':'static artifact checks only','status':'PASS' if not errors else 'FAIL','counts':counts,'errors':errors,'browser_testing':'NOT_RUN','NORM_product_testing':'NOT_RUN'}
print(json.dumps(result,indent=2))
sys.exit(bool(errors))
