// Print each materials/<lang>/cloud-product-sheet.html to PDF (one A4 page) and remove the HTML. Run after build_materials.py.
// `node print_pdf.js logo` renders assets/logo.png from assets/logo.svg instead.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
(async () => {
  const browser = await chromium.launch();
  if (process.argv[2] === 'logo') {
    const page = await browser.newPage({ viewport: { width: 256, height: 256 } });
    await page.setContent(`<body style="margin:0">${fs.readFileSync(path.join(root, 'website/assets/logo.svg'), 'utf8').replace('<svg ', '<svg width="256" height="256" ')}</body>`);
    await page.screenshot({ path: path.join(root, 'materials/assets/logo.png'), omitBackground: true });
  } else {
    for (const lang of fs.readdirSync(path.join(root, 'materials'))) {
      const src = path.join(root, 'materials', lang, 'cloud-product-sheet.html');
      if (!fs.existsSync(src)) continue;
      const page = await browser.newPage();
      await page.goto('file://' + src);
      await page.evaluate(() => document.fonts.ready);
      const over = await page.evaluate(() => { const f = document.querySelector('footer').getBoundingClientRect().top; const s = document.querySelector('.sample').getBoundingClientRect().bottom; return Math.round(f - s); });
      await page.pdf({ path: src.replace('.html', '.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
      if (process.argv[2] !== 'keep') fs.unlinkSync(src);
      console.log(lang, 'room above footer (px):', over);
      await page.close();
    }
  }
  await browser.close();
})();
