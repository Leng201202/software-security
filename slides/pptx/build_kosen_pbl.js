// KOSEN Week 10–15 PowerPoint export from the same Markdown used by /learn.
// Visual system follows KOSEN69-PBL/slides/pbl4/week03-sprint1/PBL4_W03_Sprint1.pptx:
// 16:9 light canvas, blue kicker, large navy title, KOSEN-KMITL logo,
// white evidence cards, orange emphasis and a quiet footer.
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const { parseDeck, organize, loadImage, strip } = require('./build_all');

const ROOT = path.resolve(__dirname, '..', '..');
const SLIDES = path.join(ROOT, 'slides');
const LOGO = path.join(__dirname, 'assets', 'logo-small.png');
const OUT = process.env.OUT_DIR || __dirname;
const BG = 'F4F7FB', WHITE = 'FFFFFF', NAVY = '111827';
const BLUE = '007BC4', ORANGE = 'E35205', MUTED = '606B7B', BORDER = 'D2DCE8';
const W = 13.333, H = 7.5, X = 0.58, CW = 12.15, TOP = 1.86, BOTTOM = 6.85;
const FONT = 'Arial';

function wrap(text, chars) {
  return String(text).split('\n').reduce((n, line) => n + Math.max(1, Math.ceil(line.length / chars)), 0);
}

function splitLongText(text, limit = 500) {
  if (text.length <= limit) return [text];
  const sentences = text.replace(/\s+/g, ' ').split(/(?<=[.!?])\s+/);
  const parts = [];
  let current = '';
  for (const sentence of sentences) {
    if (current && current.length + sentence.length + 1 > limit) {
      parts.push(current);
      current = '';
    }
    if (sentence.length <= limit) {
      current += (current ? ' ' : '') + sentence;
      continue;
    }
    // A single unusually long sentence still needs a bounded text box.
    for (const word of sentence.split(/\s+/)) {
      if (current && current.length + word.length + 1 > limit) {
        parts.push(current);
        current = '';
      }
      current += (current ? ' ' : '') + word;
    }
  }
  if (current) parts.push(current);
  return parts;
}

function rect(pptx, slide, x, y, w, h, fill = WHITE, border = BORDER) {
  slide.addShape(pptx.shapes.RECTANGLE, {
    x, y, w, h, rectRadius: 0, fill: { color: fill },
    line: { color: border, width: 0.8 },
  });
}

function addChrome(pptx, slide, week, title, page, label = '') {
  slide.background = { color: BG };
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: X, y: 0.49, w: 0.08, h: 0.08,
    line: { color: BLUE, transparency: 100 }, fill: { color: BLUE },
  });
  slide.addText(`SOFTWARE SECURITY 2 / WEEK ${week}${label ? ' · ' + label : ''}`, {
    x: 0.78, y: 0.36, w: 9.6, h: 0.32, margin: 0,
    fontFace: FONT, fontSize: 13, bold: true, color: BLUE, charSpacing: 1,
  });
  slide.addImage({ path: LOGO, x: 10.96, y: 0.35, w: 1.78, h: 0.84 });
  slide.addText(title, {
    x: X, y: 0.87, w: 11.7, h: 0.76, margin: 0,
    fontFace: FONT, fontSize: title.length > 52 ? 29 : 34,
    bold: true, color: NAVY, breakLine: false, fit: 'shrink',
  });
  slide.addText(`KOSEN-KMITL | Software Security 2 · Week ${week}`, {
    x: X, y: 7.03, w: 9.6, h: 0.23, margin: 0,
    fontFace: FONT, fontSize: 9, color: MUTED,
  });
  slide.addText(String(page), {
    x: 12.28, y: 7.01, w: 0.4, h: 0.25, margin: 0,
    fontFace: FONT, fontSize: 10, color: MUTED, align: 'right',
  });
}

function drawText(pptx, slide, kind, text, y) {
  const isQuote = kind === 'quote';
  const lines = wrap(text, isQuote ? 75 : 85);
  const h = Math.min(4.75, Math.max(isQuote ? 0.82 : 0.65, 0.34 * lines + 0.31));
  rect(pptx, slide, X, y, CW, h, isQuote ? NAVY : WHITE, isQuote ? NAVY : BORDER);
  if (!isQuote) slide.addShape(pptx.shapes.RECTANGLE, {
    x: X, y, w: 0.09, h,
    line: { color: BLUE, transparency: 100 }, fill: { color: BLUE },
  });
  slide.addText(text, {
    x: X + 0.28, y: y + 0.12, w: CW - 0.55, h: h - 0.22,
    margin: 0, fontFace: FONT, fontSize: isQuote ? 18 : 17,
    color: isQuote ? WHITE : NAVY, bold: isQuote,
    valign: 'mid', fit: 'shrink', breakLine: false,
  });
  return h;
}

function drawBullets(pptx, slide, bullets, y) {
  const heights = bullets.map(b => Math.max(0.46, 0.34 * wrap(b.text, b.lvl ? 95 : 104) + 0.12));
  const h = Math.min(4.72, heights.reduce((a, b) => a + b, 0) + 0.24);
  rect(pptx, slide, X, y, CW, h);
  let by = y + 0.17;
  for (let i = 0; i < bullets.length; i++) {
    const b = bullets[i], bh = heights[i];
    slide.addShape(pptx.shapes.OVAL, {
      x: X + (b.lvl ? 0.58 : 0.32), y: by + 0.13, w: 0.12, h: 0.12,
      line: { color: b.lvl ? ORANGE : BLUE, transparency: 100 },
      fill: { color: b.lvl ? ORANGE : BLUE },
    });
    slide.addText(b.text, {
      x: X + (b.lvl ? 0.86 : 0.60), y: by,
      w: CW - (b.lvl ? 1.15 : 0.9), h: bh,
      margin: 0, fontFace: FONT, fontSize: 17, color: NAVY,
      valign: 'mid', fit: 'shrink',
    });
    by += bh;
  }
  return h;
}

function drawNumbered(pptx, slide, numbers, y) {
  const heights = numbers.map(t => Math.max(0.52, 0.34 * wrap(t, 100) + 0.14));
  const h = Math.min(4.75, heights.reduce((a, b) => a + b, 0) + 0.22);
  rect(pptx, slide, X, y, CW, h);
  let by = y + 0.13;
  for (let i = 0; i < numbers.length; i++) {
    slide.addShape(pptx.shapes.OVAL, {
      x: X + 0.23, y: by + 0.04, w: 0.35, h: 0.35,
      line: { color: BLUE, transparency: 100 }, fill: { color: BLUE },
    });
    slide.addText(String(i + 1), {
      x: X + 0.23, y: by + 0.04, w: 0.35, h: 0.35,
      margin: 0, fontFace: FONT, fontSize: 14, bold: true,
      color: WHITE, align: 'center', valign: 'mid',
    });
    slide.addText(numbers[i], {
      x: X + 0.76, y: by, w: CW - 1.0, h: heights[i],
      margin: 0, fontFace: FONT, fontSize: 17, color: NAVY,
      valign: 'mid', fit: 'shrink',
    });
    by += heights[i];
  }
  return h;
}

function drawCode(pptx, slide, lines, y) {
  const h = Math.min(4.72, Math.max(0.8, 0.29 * lines.length + 0.35));
  rect(pptx, slide, X, y, CW, h, NAVY, NAVY);
  slide.addText(lines.join('\n'), {
    x: X + 0.28, y: y + 0.16, w: CW - 0.56, h: h - 0.3,
    margin: 0, fontFace: 'Courier New', fontSize: 13,
    color: 'D4F6EC', valign: 'top', fit: 'shrink',
  });
  return h;
}

function drawTable(pptx, slide, rows, y) {
  const h = Math.min(4.72, 0.55 * rows.length);
  const ncol = Math.max(...rows.map(r => r.length));
  slide.addTable(rows.map((row, ri) => Array.from({ length: ncol }, (_, ci) => ({
    text: row[ci] || '', options: {
      fontFace: FONT, fontSize: ri === 0 ? 14 : 13,
      bold: ri === 0, color: ri === 0 ? WHITE : NAVY,
      fill: { color: ri === 0 ? BLUE : (ri % 2 ? WHITE : 'EAF2F8') },
      margin: 0.08, valign: 'mid',
    },
  }))), {
    x: X, y, w: CW, h, rowH: h / rows.length,
    colW: Array(ncol).fill(CW / ncol),
    border: { type: 'solid', color: BORDER, pt: 0.7 },
  });
  return h;
}

function drawImage(pptx, slide, img, alt, y) {
  const maxW = CW - 0.38, maxH = BOTTOM - y - 0.36;
  const scale = Math.min(maxW / img.w, maxH / img.h);
  const w = img.w * scale, h = img.h * scale;
  rect(pptx, slide, X, y, CW, h + 0.34);
  slide.addImage({ data: img.data, x: X + (CW - w) / 2, y: y + 0.16, w, h, altText: alt });
  return h + 0.34;
}

function chunks(items, count) {
  const out = [];
  for (let i = 0; i < items.length; i += count) out.push(items.slice(i, i + count));
  return out;
}

async function build(week) {
  if (!Number.isInteger(week) || week < 10 || week > 15) {
    throw new Error('This exporter accepts only the fixed KOSEN Week 10–15 range');
  }
  const ww = String(week).padStart(2, '0');
  // `week` is validated above and the caller enumerates literal weeks only.
  const md = fs.readFileSync(path.join(SLIDES, `week${ww}.md`), 'utf8'); // nosemgrep: javascript.lang.security.audit.path-traversal.path-join-resolve-traversal.path-join-resolve-traversal
  const blocks = parseDeck(md);
  if (process.env.DEBUG_DECK) console.log(`Week ${week}: parsed ${blocks.length} blocks`);
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_WIDE';
  pptx.author = 'Nutthakorn Chalaemwongwan';
  pptx.subject = `KOSEN Software Security 2 Week ${week}`;
  pptx.title = `Week ${week} — ${blocks[0].title}`;
  pptx.lang = 'en-US';
  let page = 0;
  const addPage = (title, label = '') => {
    const slide = pptx.addSlide();
    addChrome(pptx, slide, week, title, ++page, label);
    return slide;
  };

  const cover = addPage(blocks[0].title || `Week ${week}`, 'KOSEN');
  const today = organize(blocks[1].body).find(it => it.kind === 'bullets');
  const points = today ? today.items.slice(0, 3).map(it => it.text) : [];
  cover.addText(`Week ${week}`, {
    x: X, y: 2.02, w: 6.9, h: 0.55, margin: 0,
    fontFace: FONT, fontSize: 26, bold: true, color: BLUE,
  });
  cover.addText('Software Security 2', {
    x: X, y: 2.75, w: 7.0, h: 0.62, margin: 0,
    fontFace: FONT, fontSize: 30, color: NAVY,
  });
  cover.addText(strip((blocks[0].body.find(b => b.t === 'raw') || {}).v || ''), {
    x: X, y: 3.68, w: 7.2, h: 0.6, margin: 0,
    fontFace: FONT, fontSize: 17, color: MUTED,
  });
  cover.addText('Today', {
    x: 8.08, y: 1.85, w: 4.45, h: 0.36, margin: 0,
    fontFace: FONT, fontSize: 18, bold: true, color: MUTED,
  });
  points.forEach((point, i) => {
    const y = 2.34 + i * 1.22;
    rect(pptx, cover, 8.08, y, 4.52, 1.05);
    cover.addShape(pptx.shapes.OVAL, {
      x: 8.35, y: y + 0.32, w: 0.34, h: 0.34,
      line: { color: i === 1 ? ORANGE : BLUE, transparency: 100 },
      fill: { color: i === 1 ? ORANGE : BLUE },
    });
    cover.addText(point, {
      x: 8.91, y: y + 0.16, w: 3.4, h: 0.72,
      margin: 0, fontFace: FONT, fontSize: 16,
      bold: true, color: NAVY, fit: 'shrink', valign: 'mid',
    });
  });
  if (blocks[0].notes) cover.addNotes(blocks[0].notes);

  for (let bi = 1; bi < blocks.length; bi++) {
    const block = blocks[bi];
    if (process.env.DEBUG_DECK) console.log(`Week ${week}: block ${bi} ${block.title || block.h1}`);
    const title = block.title || block.h1 || `Week ${week}`;
    const items = organize(block.body);
    if (process.env.DEBUG_DECK) console.log(`Week ${week}: ${items.length} items`);
    let slide = addPage(title), y = TOP;
    const blockSlides = [slide];
    const next = () => { slide = addPage(title + ' (cont.)'); blockSlides.push(slide); y = TOP; };
    const place = (height, action) => {
      if (y + height > BOTTOM && y > TOP + 0.05) next();
      const used = action();
      y += used + 0.16;
    };
    for (const it of items) {
      if (it.kind === 'image') {
        const img = await loadImage(ww, it.src);
        if (!img) throw new Error(`Week ${week}: missing diagram ${it.src}`);
        if (y > TOP + 0.4) next();
        y += drawImage(pptx, slide, img, it.alt || 'diagram', y) + 0.16;
      } else if (it.kind === 'bullets') {
        for (const part of chunks(it.items, 7)) {
          const est = Math.min(4.72, part.reduce((h, b) => h + Math.max(0.46, 0.34 * wrap(b.text, b.lvl ? 95 : 104) + 0.12), 0) + 0.24);
          place(est, () => drawBullets(pptx, slide, part, y));
        }
      } else if (it.kind === 'numbered') {
        for (const part of chunks(it.items, 7)) {
          const est = Math.min(4.75, part.reduce((h, t) => h + Math.max(0.52, 0.34 * wrap(t, 100) + 0.14), 0) + 0.22);
          place(est, () => drawNumbered(pptx, slide, part, y));
        }
      } else if (it.kind === 'code') {
        for (const lines of chunks(it.text.split('\n'), 15)) {
          const est = Math.min(4.72, Math.max(0.8, 0.29 * lines.length + 0.35));
          place(est, () => drawCode(pptx, slide, lines, y));
        }
      } else if (it.kind === 'table') {
        for (const part of chunks(it.rows.slice(1), 7)) {
          const rows = [it.rows[0], ...part];
          const est = Math.min(4.72, 0.55 * rows.length);
          place(est, () => drawTable(pptx, slide, rows, y));
        }
      } else if (it.kind === 'quote' || it.kind === 'para') {
        for (const part of splitLongText(it.text)) {
          const est = Math.min(4.75, Math.max(it.kind === 'quote' ? 0.82 : 0.65, 0.34 * wrap(part, it.kind === 'quote' ? 75 : 85) + 0.31));
          place(est, () => drawText(pptx, slide, it.kind, part, y));
        }
      }
    }
    if (block.notes) blockSlides.forEach(s => s.addNotes(block.notes));
  }
  fs.mkdirSync(OUT, { recursive: true });
  const dest = path.join(OUT, `week${ww}.pptx`); // nosemgrep: javascript.lang.security.audit.path-traversal.path-join-resolve-traversal.path-join-resolve-traversal
  await pptx.writeFile({ fileName: dest });
  console.log(`${dest} | ${page} slides | ${blocks.length} source blocks`);
}

(async () => {
  for (const week of [10, 11, 12, 13, 14, 15]) await build(week);
})().catch(err => { console.error(err); process.exitCode = 1; });
