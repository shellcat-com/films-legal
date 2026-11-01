// Run from the repository root: node scripts/build-brand.cjs [path/to/icon-1024.png]
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('../site/node_modules/sharp');
const root = path.resolve(__dirname, '..');
const mark = fs.readFileSync(path.join(root, 'brand/filmsera-mark.svg'), 'utf8');
const inner = mark.match(/<svg[^>]*>([\s\S]*)<\/svg>/)[1];
const scale = 560 / 660;
const iconSvg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><rect width="1024" height="1024" fill="#0A0807"/><g transform="translate(${(1024-560*scale)/2} 232) scale(${scale})">${inner}</g></svg>`;
(async () => {
  const icon = path.join(root, 'shots/filmsera-icon.png');
  if (process.argv[2]) fs.copyFileSync(process.argv[2], icon);
  fs.writeFileSync(path.join(root, 'favicon.svg'), iconSvg + '\n');
  for (const size of [16, 32, 96, 180, 512]) {
    await sharp(Buffer.from(iconSvg)).resize(size, size).png().toFile(path.join(root, `favicon-${size}.png`));
  }
  fs.copyFileSync(path.join(root, 'favicon-180.png'), path.join(root, 'apple-touch-icon.png'));
  // ICO directory with PNG entries (supported by modern browsers and Windows).
  const sizes = [16, 32];
  const frames = sizes.map(s => fs.readFileSync(path.join(root, `favicon-${s}.png`)));
  const header = Buffer.alloc(6 + 16 * frames.length);
  header.writeUInt16LE(1, 2); header.writeUInt16LE(frames.length, 4);
  let offset = header.length;
  frames.forEach((frame, i) => {
    const p = 6 + i * 16;
    header[p] = sizes[i]; header[p+1] = sizes[i];
    header.writeUInt16LE(1, p+4); header.writeUInt16LE(32, p+6);
    header.writeUInt32LE(frame.length, p+8); header.writeUInt32LE(offset, p+12);
    offset += frame.length;
  });
  fs.writeFileSync(path.join(root, 'favicon.ico'), Buffer.concat([header, ...frames]));
  // Social cards use the exact app raster, on a 1200×630 ink canvas.
  await sharp({create: {width:1200,height:630,channels:3,background:'#0A0807'}})
    .composite([{input:await sharp(icon).resize(630,630).toBuffer(),left:285,top:0}])
    .png().toFile(path.join(root, 'shots/filmsera-social.png'));
  for (const name of ['favicon.svg','favicon.ico','apple-touch-icon.png', ...[16,32,96,180,512].map(s=>`favicon-${s}.png`)]) {
    fs.copyFileSync(path.join(root,name),path.join(root,'site/public',name));
  }
  fs.mkdirSync(path.join(root,'site/public/brand'),{recursive:true});
  fs.copyFileSync(path.join(root,'brand/filmsera-mark.svg'),path.join(root,'site/public/brand/filmsera-mark.svg'));
  for (const name of ['filmsera-icon.png','filmsera-social.png']) fs.copyFileSync(path.join(root,'shots',name),path.join(root,'site/public/shots',name));
})().catch(error => { console.error(error); process.exitCode = 1; });
