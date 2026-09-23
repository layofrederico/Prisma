// Renderiza quadro a quadro: para cada slide, posiciona o tempo e fotografa. Uso:
//   node renderiza.js <plano.json> <pasta_quadros> [fps]
// plano.json = [{"slide": "Capa", "dur": 5.7}, ...]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const plano = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const pasta = process.argv[3];
  const fps = Number(process.argv[4] || 30);
  fs.mkdirSync(pasta, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  let n = 0;
  for (const item of plano) {
    await page.goto('file://' + path.resolve(__dirname, 'paginas', item.slide + '.html'));
    await page.evaluate(() => document.fonts.ready);
    const fontes = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').length);
    if (fontes === 0) throw new Error('Poppins não carregou em ' + item.slide);
    const quadros = Math.round(item.dur * fps);
    const soQuadros = item.quadros || null;  // teste: fotografa só alguns instantes
    const instantes = soQuadros ? soQuadros : [...Array(quadros).keys()].map(i => i / fps);
    for (const t of instantes) {
      await page.evaluate(tt => window.__setTime(tt), t);
      n += 1;
      await page.screenshot({ path: path.join(pasta, String(n).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92 });
    }
    process.stdout.write(item.slide + ' ');
  }
  await browser.close();
  console.log('\nquadros:', n);
})().catch(e => { console.error(e.message); process.exit(1); });
