import { createRequire } from 'node:module';
const pw = createRequire(process.env.NODE_PATH + '/x.js')('playwright');
const b = await pw.chromium.launch({ headless: true });
const p = await b.newPage({ viewport: { width: 2400, height: 1400 }, deviceScaleFactor: 2 });
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('file://' + process.cwd() + '/render.html');
await p.waitForTimeout(1500);
await (await p.$('#s')).screenshot({ path: 'duo.png', omitBackground: true });
await b.close(); console.log('ok', errs.join(';'));
