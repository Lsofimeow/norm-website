"""Build explicit Chinese routes; no runtime translation or browser storage."""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
import json
import posixpath
import re
import xml.etree.ElementTree as ET

ATTRS = {'alt', 'aria-label', 'title', 'data-caption'}

class ChinesePage(HTMLParser):
    def __init__(self, translations, path, base, collect=False):
        super().__init__(convert_charrefs=True)
        self.translations=translations; self.path=path; self.base=base
        self.out=[]; self.raw=None; self.missing=set(); self.collect=collect

    def tr(self, value):
        key=value.strip()
        if not key or not re.search(r'[A-Za-z]', key): return value
        if key in self.translations: return value.replace(key,self.translations[key])
        if re.fullmatch(r'(NORM|AI|EN|Windows|NORM / \d+|hello@normautonomy.com)',key): return value
        if key.startswith('Enlarge screenshot: '): return '放大截图：'+self.tr(key[len('Enlarge screenshot: '):])
        if key.endswith(' | NORM'): return self.tr(key[:-7])+' | NORM'
        if re.match(r'^0\d / ',key): return key[:5]+self.tr(key[5:])
        if key.startswith('Illustrated workflow · '): return key.replace('Illustrated workflow','流程示意')
        self.missing.add(key)
        return value

    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'viewbox' in a: a['viewBox']=a.pop('viewbox')
        if tag in ('style','script'): self.raw=tag
        if tag=='html': a['lang']='zh-CN'
        for key in ATTRS & a.keys(): a[key]=self.tr(a[key])
        if tag=='meta' and a.get('name',a.get('property')) in ('description','og:title','og:description','og:image:alt'):
            a['content']=self.tr(a['content'])
        if tag=='meta' and a.get('property')=='og:url': a['content']=self.canonical()
        if tag=='link' and a.get('rel')=='canonical': a['href']=self.canonical()
        language=a.get('data-language')
        if language:
            target=self.path if language=='en' else 'zh/'+self.path
            a['href']=posixpath.relpath(target,posixpath.dirname('zh/'+self.path))
            if self.path=='404.html': a['href']=self.base+'/'+target
            if language=='zh': a['aria-current']='true'
            else: a.pop('aria-current',None)
        else:
            for key in ('href','src','data-screen'):
                if key not in a: continue
                val=a[key]
                if not val.startswith(('http:','https:','mailto:','#')) and re.search(r'(?:^|/)(assets|css|js)/|favicon\.svg',val):
                    val='../'+val
                    if 'assets/workspace-architecture.svg' in val or 'assets/waypoint-plan.svg' in val:
                        val=val.replace('assets/','assets/zh/')
                    a[key]=val
                elif tag=='a' and val.startswith(self.base+'/'):
                    a[key]=self.base+'/zh/'+val[len(self.base)+1:]
        self.out.append('<'+tag+''.join(' '+k+('="'+escape(v,quote=True)+'"' if v is not None else '') for k,v in a.items())+'>')

    def canonical(self):
        return self.base+'/zh/'+self.path.replace('index.html','')

    def handle_endtag(self,tag):
        self.out.append('</'+tag+'>')
        if tag==self.raw:self.raw=None

    def handle_data(self,value): self.out.append(value if self.raw else escape(self.tr(value),quote=False))
    def handle_decl(self,value): self.out.append('<!'+value+'>')
    def handle_comment(self,value): self.out.append('<!--'+value+'-->')

def build_chinese(root, dist, paths, base):
    translations=json.loads((root/'src/i18n/zh-CN.json').read_text())
    missing=set()
    for path in paths:
        parser=ChinesePage(translations,path,base)
        parser.feed((dist/path).read_text())
        missing.update(parser.missing)
        target=dist/'zh'/path;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(''.join(parser.out),encoding='utf-8')
    ET.register_namespace('','http://www.w3.org/2000/svg')
    for name in ('waypoint-plan.svg','workspace-architecture.svg'):
        tree=ET.parse(dist/'assets'/name)
        for node in tree.iter():
            if node.text and node.text.strip(): node.text=parser.tr(node.text)
        target=dist/'assets/zh'/name;target.parent.mkdir(parents=True,exist_ok=True)
        tree.write(target,encoding='utf-8',xml_declaration=True)
    missing.update(parser.missing)
    if missing: raise SystemExit('Missing Chinese translations:\n'+json.dumps(sorted(missing),ensure_ascii=False,indent=2))
