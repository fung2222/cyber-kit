# cyber-kit

> CYBER ARCADE 共用引擎 · shared cyberpunk 3D game kit · Three.js r169 · ES modules · 冇 build step

由 [CYBER SNAKE 賽博蛇](https://github.com/fung2222/cyber-snake) 抽出嚟嘅共用代碼：霓虹城市背景、bloom + 故障後製、粒子、衝擊波、合成音效同音樂、觸控/鍵盤輸入、HUD/畫面/對話框、本機儲存、Android (Capacitor) 平台掛鈎同 AdMob 廣告封裝。

**Playground:** https://fung2222.github.io/cyber-kit/examples/

## 用法 Usage
每隻遊戲將某個 **tag 版本** 複製入 `vendor/cyber-kit/`（唔用 CDN，方便離線同包 App）：
```bash
git clone --depth 1 --branch v0.2.0 https://github.com/fung2222/cyber-kit /tmp/ck
mkdir -p vendor/cyber-kit && (cd /tmp/ck && tar cf - --exclude=.git --exclude=examples --exclude=docs --exclude=README.md .) | (cd vendor/cyber-kit && tar xf -)
```
```html
<link rel="stylesheet" href="./vendor/cyber-kit/ui/hud.css">
<script type="importmap">
{ "imports": {
  "three": "./vendor/cyber-kit/three/three.module.min.js",
  "three/addons/": "./vendor/cyber-kit/three/addons/",
  "cyber-kit": "./vendor/cyber-kit/kit.js",
  "cyber-kit/": "./vendor/cyber-kit/" } }
</script>
```
```js
import { createStage, NeonCity, ThemeController, SynthAudio, createInput, CyberUI, createStore } from 'cyber-kit';
const stage = createStage({ canvas: document.querySelector('canvas') });
const theme = new ThemeController(); theme.set(1, true);
const city = new NeonCity(stage, { billboard: { zh: '賽博', en: 'C Y B E R' } });
stage.loop((dt, t) => { theme.update(dt); city.update(t, dt, stage.camera); stage.render(dt); });
```

## 模組 Modules
| Path | 內容 |
|---|---|
| `core/flags.js` | URL 參數 `?demo=1&fps=1&quality=low&adsim=1…` |
| `core/storage.js` | `createStore(gameId)` → localStorage `cyber.<game>.<key>` |
| `core/theme.js` | 共用 uniforms `U`、6 個香港地區色系 `THEMES`、`ThemeController` |
| `core/renderer.js` | `createStage()`：renderer + bloom + CyberShader + resize + loop + 自動畫質 |
| `core/post.js` | `CyberShader` 色差 / 故障 / 暗角 / 噪點 |
| `core/fx.js` | `Particles`、`Shockwaves`、`FxState`（震動、色差、慢鏡） |
| `core/backdrop.js` | `NeonCity`：天空、反射地面、大廈、招牌、雨、車流 |
| `audio/synth.js` | `SynthAudio`：合成音效 + 音樂（drive / chill） |
| `input/input.js` | `createInput()`：滑動、點擊、長按、鍵盤動作 |
| `ui/ui.js` + `ui/hud.css` | `CyberUI`：畫面切換、橫幅、彈字、toast、確認對話框 |
| `platform/platform.js` | `Platform`：Android 返回鍵、暫停/恢復、震動 |
| `platform/ads.js` | `createAds()`：AdMob (`@capacitor-community/admob` v8) + UMP 同意；網頁版無廣告 |

完整 API：[docs/API.md](docs/API.md)

## 版本 Versions
- **v0.2.0** (2026-10-02) — 首個版本，用於 DATA FUSE。

## 授權 License
Kit code: MIT © fung2222. Three.js: MIT (`three/LICENSE`). Orbitron font: SIL OFL 1.1 (`fonts/OFL.txt`).

## v0.2.1
- `addStrings()` auto-repaints `data-i18n` elements (no manual `i18n.apply()` needed); glitch titles keep `data-text` in sync.

## v0.2.0
- **i18n** (`core/i18n.js`): zh-HK / English, `t(key)`, per-game string tables, live DOM updates via `data-i18n`, toggle button, choice stored in `localStorage['cyber.lang']`. See [docs/API.md](docs/API.md#corei18njs-v020--bilingual-zh-hk--en).
- **endless helpers** (`core/endless.js`): capped difficulty curve + milestones.
- Kit UI/ads-sim/WebGL-error strings are now translated.
