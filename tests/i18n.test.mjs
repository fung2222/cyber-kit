// node tests/i18n.test.mjs — i18n + endless helpers (no DOM)
import assert from 'node:assert/strict';
import { t, addStrings, setLang, getLang, onLangChange, tBoth, detectLang } from '../core/i18n.js';
import { endlessCurve, milestoneOf } from '../core/endless.js';
let n = 0; const ok = (name, fn) => { fn(); n++; console.log('ok - ' + name); };
ok('kit strings registered', () => { setLang('zh-HK', { persist: false }); assert.equal(t('kit.paused'), '已暫停'); setLang('en', { persist: false }); assert.equal(t('kit.paused'), 'PAUSED'); });
ok('pairs + objects + params', () => { addStrings({ fl: ['第 {n} 層', 'FLOOR {n}'], o: { 'zh-HK': '甲', en: 'A' } }); setLang('en', { persist: false }); assert.equal(t('fl', { n: 3 }), 'FLOOR 3'); assert.equal(t('o'), 'A'); setLang('zh', { persist: false }); assert.equal(getLang(), 'zh-HK'); assert.equal(t('fl', { n: 3 }), '第 3 層'); });
ok('unknown key returns key; empty en falls back to zh', () => { assert.equal(t('nope'), 'nope'); addStrings({ e: ['只有中文', ''] }); setLang('en', { persist: false }); assert.equal(t('e'), '只有中文'); });
ok('change listeners fire once per change', () => { let c = 0; const off = onLangChange(() => c++); setLang('zh-HK', { persist: false }); setLang('zh-HK', { persist: false }); setLang('en', { persist: false }); off(); setLang('zh-HK', { persist: false }); assert.equal(c, 2); });
ok('tBoth', () => assert.equal(tBoth('kit.paused'), '已暫停 PAUSED'));
ok('detectLang without browser defaults sensibly', () => assert.ok(['zh-HK', 'en'].includes(detectLang())));
ok('endlessCurve rises and is capped', () => { const a = endlessCurve(0, { start: 1, cap: 3 }), b = endlessCurve(10, { start: 1, cap: 3 }), c = endlessCurve(1e6, { start: 1, cap: 3 }); assert.equal(a, 1); assert.ok(b > a && b < 3); assert.ok(c <= 3 && c > 2.999); });
ok('milestoneOf', () => { assert.equal(milestoneOf(20, 10), 2); assert.equal(milestoneOf(21, 10), 0); assert.equal(milestoneOf(0, 10), 0); });
console.log(`ALL PASSED (${n})`);
