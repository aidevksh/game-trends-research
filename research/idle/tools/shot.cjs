// Usage: node shot.cjs <html> <outdir> [mode]
const {chromium}=require('C:/Users/FORYOUCOM/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path');
(async()=>{
  const [html,outdir,mode='full']=process.argv.slice(2);
  const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
  const url='file:///'+path.resolve(html).replace(/\\/g,'/');
  const errors=[];
  for(const [name,vp] of [['desktop',{width:1440,height:1000}],['mobile',{width:390,height:844}]]){
    const page=await browser.newPage({viewport:vp,deviceScaleFactor:1});
    page.on('pageerror',e=>errors.push(name+': '+e.message));
    page.on('console',m=>{if(m.type()==='error')errors.push(name+' console: '+m.text());});
    await page.goto(url);
    await page.addStyleTag({content:'html{scroll-behavior:auto!important}'});
    const overflow=await page.evaluate(()=>{const w=document.documentElement.clientWidth;const bad=[];for(const el of document.querySelectorAll('body *')){const r=el.getBoundingClientRect();if(r.width>0&&r.right>w+1&&!el.closest('.table-scroll')&&!el.closest('.topbar nav')){bad.push(el.tagName+'.'+el.className+' right='+Math.round(r.right));if(bad.length>8)break;}}return {scrollW:document.documentElement.scrollWidth,clientW:w,bad};});
    console.log(name,'overflow',JSON.stringify(overflow));
    const sections=['#top','#summary','#market','#genres','#recommend','#research','#compare','#design','#launch'];
    if(mode==='full'){
      for(const s of sections){
        const el=await page.$(s);if(!el)continue;
        await el.scrollIntoViewIfNeeded();
        await page.evaluate(sel=>{const e=document.querySelector(sel);window.scrollTo(0,e.getBoundingClientRect().top+scrollY-(sel==='#top'?0:70));},s);
        await page.waitForTimeout(150);
        await page.screenshot({path:path.join(outdir,`${name}-${s.slice(1)}.png`)});
      }
      // a game card and deep dive
      const card=await page.$('.game-card');
      if(card){await page.evaluate(()=>{const e=document.querySelector('.game-card');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-80);});await page.waitForTimeout(100);await page.screenshot({path:path.join(outdir,`${name}-card.png`)});}
      const dd=await page.$('.deepdive');
      if(dd){await page.evaluate(()=>{const e=document.querySelector('.deepdive');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-80);});await page.waitForTimeout(100);await page.screenshot({path:path.join(outdir,`${name}-deepdive.png`)});}
      const sim=await page.$('#sim');
      if(sim){await page.evaluate(()=>{const e=document.querySelector('#sim');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-80);});await page.waitForTimeout(100);await page.screenshot({path:path.join(outdir,`${name}-sim.png`)});}
    }
    // filter test
    const total=await page.locator('.game-card').count();
    await page.selectOption('#category-filter',{index:1});
    const afterCat=await page.locator('.game-card:visible').count();
    await page.click('#reset');
    await page.fill('#search','zzzz_not_real');
    const empty=await page.locator('#empty').isVisible();
    await page.click('#reset');
    const afterReset=await page.locator('.game-card:visible').count();
    console.log(name,'filter',{total,afterCat,empty,afterReset});
    await page.close();
  }
  console.log('errors',JSON.stringify(errors));
  await browser.close();
})();
