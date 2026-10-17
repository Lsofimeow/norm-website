// Isolated browser acceptance; no production or infrastructure changes.
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
const root=process.env.NORM_REVIEW_ROOT?resolve(process.env.NORM_REVIEW_ROOT):fileURLToPath(new URL('.',import.meta.url));
const mime={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.png':'image/png','.json':'application/json'};
const server=createServer(async(req,res)=>{try{const p=resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://local').pathname));if(!p.startsWith(root.endsWith(sep)?root:root+sep))throw Error('Invalid path');const bytes=await readFile(p);res.writeHead(200,{'Content-Type':mime[extname(p)]||'application/octet-stream'});res.end(bytes)}catch{res.writeHead(404);res.end('Not found')}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base='http://127.0.0.1:'+server.address().port;
const results={scope:'Local website browser checks, not NORM product testing',started_at:new Date().toISOString(),revision:process.env.NORM_REVISION||'local',run_url:process.env.NORM_RUN_URL||null,screenshots:[],checks:[],errors:[]};
let browser;
try{
 browser=await chromium.launch();results.browser=browser.version();results.engine='Chromium';results.device_scale_factor=1;await mkdir(resolve(root,'screenshots'),{recursive:true});
 for(const stage of ['before','after'])for(const width of [1440,768,390])for(const language of stage==='after'?['en','zh']:['en'])for(const [name,route]of[['home','index.html'],['platform','platform/index.html']]){
  const context=await browser.newContext({viewport:{width,height:({1440:1000,768:900,390:844})[width]},deviceScaleFactor:1,reducedMotion:'reduce'});const page=await context.newPage();page.setDefaultTimeout(15000);
  const label=[stage,language,name,width].join('-');
  page.on('pageerror',e=>results.errors.push({label,type:'pageerror',message:e.message}));page.on('console',m=>{if(m.type()==='error')results.errors.push({label,type:'console',message:m.text()})});page.on('response',r=>{if(r.status()>=400)results.errors.push({label,type:'http',status:r.status(),url:r.url()})});page.on('requestfailed',r=>results.errors.push({label,type:'requestfailed',url:r.url()}));
  const path=stage+'/'+(language==='zh'?'zh/':'')+route;await page.goto(base+'/'+path,{waitUntil:'networkidle'});
  await page.evaluate(async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));await document.fonts.ready});
  await page.screenshot({path:resolve(root,'screenshots',label+'-full.png'),fullPage:true});await page.screenshot({path:resolve(root,'screenshots',label+'-hero.png')});results.screenshots.push({label,width,path:'screenshots/'+label+'-full.png',hero:'screenshots/'+label+'-hero.png'});
  const overflow=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,elements:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1&&getComputedStyle(e).position!=='fixed'&&e.getBoundingClientRect().width>0).slice(0,12).map(e=>({tag:e.tagName,class:e.className,right:e.getBoundingClientRect().right}))}));results.checks.push({label,check:'root_horizontal_overflow',status:overflow.overflow?'FAIL':'PASS',details:overflow});
  const broken=await page.evaluate(()=>[...document.images].filter(i=>i.src&&(!i.complete||!i.naturalWidth)).map(i=>i.src));results.checks.push({label,check:'images_loaded',status:broken.length?'FAIL':'PASS',broken});
  if(stage==='after'){
   const subtitle=await page.locator('.hero-subtitle').innerText();
   results.checks.push({label,check:'subtitle_word_spacing',status:language!=='en'||(!subtitle.includes('review.Built')&&!subtitle.includes('edits,and'))?'PASS':'FAIL',subtitle});
   if(name==='platform'){
    await page.locator('.hero-center .button').click();
    results.checks.push({label,check:'workspace_cta_destination',status:page.url().endsWith('#workspace')&&await page.locator('#workspace').isVisible()?'PASS':'FAIL'});
   }
   if(width<992){await page.locator('.menu-toggle').click();const opened=await page.locator('.menu-toggle').getAttribute('aria-expanded')==='true';await page.keyboard.press('Escape');const closed=await page.locator('.menu-toggle').getAttribute('aria-expanded')==='false';results.checks.push({label,check:'menu_open_and_escape',status:opened&&closed?'PASS':'FAIL'})}
   await page.locator('[data-screen]').first().click();const open=await page.locator('.screen-dialog').evaluate(e=>e.open);await page.keyboard.press('Escape');const close=await page.locator('.screen-dialog').evaluate(e=>!e.open);const focus=await page.locator('[data-screen]').first().evaluate(e=>e===document.activeElement);results.checks.push({label,check:'image_dialog_and_focus',status:open&&close&&focus?'PASS':'FAIL'});
   await page.locator('[data-step="4"]').click();results.checks.push({label,check:'workflow_stage',status:await page.locator('[data-panel="4"]').isVisible()?'PASS':'FAIL'});
   const target=language==='en'?'zh':'en';await page.locator('[data-language="'+target+'"]').click();const expected=base+'/after/'+(target==='zh'?'zh/':'')+route;results.checks.push({label,check:'language_keeps_route',status:page.url()===expected?'PASS':'FAIL'});
  }
  await context.close();
 }
 const manifest=JSON.parse(await readFile(resolve(root,'after/BUILD_MANIFEST.json'),'utf8'));
 for(const width of [1440,768,390]){
 const page=await browser.newPage({viewport:{width,height:900}});let current='';
 page.on('pageerror',e=>results.errors.push({label:current,type:'pageerror',message:e.message}));
 page.on('console',m=>{if(m.type()==='error')results.errors.push({label:current,type:'console',message:m.text()})});
 page.on('response',r=>{if(r.status()>=400)results.errors.push({label:current,type:'http',status:r.status(),url:r.url()})});
 for(const file of Object.keys(manifest.files).filter(f=>f.endsWith('.html'))){
  current=file+'@'+width;const response=await page.goto(base+'/after/'+file,{waitUntil:'networkidle'});
  const layout=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,h1:document.querySelectorAll('h1').length,broken:[...document.images].filter(i=>i.getAttribute('src')&&i.complete&&!i.naturalWidth).map(i=>i.src)}));
  results.checks.push({label:current,check:'route_layout_resources',status:response.status()===200&&!layout.overflow&&layout.h1===1&&!layout.broken.length?'PASS':'FAIL',details:layout});
  if(!file.endsWith('404.html')){
   if(width<992)await page.locator('.menu-toggle').click();
   await page.locator('.nav-contact').click();
   results.checks.push({label:current,check:'contact_navigation',status:page.url()===base+'/after/'+(file.startsWith('zh/')?'zh/':'')+'contact/index.html'?'PASS':'FAIL'});
  }
 }
 await page.close();
 }
 results.status=results.errors.length||results.checks.some(c=>c.status==='FAIL')?'FAIL':'PASS';
}catch(error){results.status='FAIL';results.errors.push({type:'runner',message:String(error)})}
finally{if(browser)await browser.close();await new Promise(r=>server.close(r));results.finished_at=new Date().toISOString();await writeFile(resolve(root,'browser-results.json'),JSON.stringify(results,null,2));console.log(results.status,'— see browser-results.json');if(results.status!=='PASS')process.exitCode=1}
