# cyber-kit API (v0.2.1)

All modules are plain ES modules. Import from `'cyber-kit'` (everything) or deep paths like `'cyber-kit/core/theme.js'` (same module instances).

## core/flags.js
`parseFlags(search?)` → object; `flags` = parsed `location.search`.
| flag | type | meaning |
|---|---|---|
| `demo` | bool | AI autoplay / attract demo |
| `autostart` | bool | skip start screen |
| `level` | int | start level |
| `fps` | bool | show FPS meter |
| `noauto` | bool | disable auto-quality |
| `quality` | low/med/high/auto | pixel-ratio cap (low also drops floor reflection) |
| `bloom`, `exp`, `tm`, `dtcap` | number/string | bloom strength, exposure, tone mapping, dt cap |
| `seed` | int | deterministic RNG seed (game-defined) |
| `adsim` | bool | simulate ad overlays in the browser |
| `mute`, `reset`, `debug` | bool | start muted, clear storage, verbose logs |

## core/i18n.js (v0.2.0) — bilingual zh-HK / en
Every CYBER game must be bilingual (Traditional Chinese, Hong Kong + English) with an in-game toggle.
- Language codes: `LANGS = ['zh-HK', 'en']`. Choice persisted in **`localStorage['cyber.lang']`** (shared by all CYBER games, not namespaced per game).
- Default (`detectLang()`): `?lang=en|zh` URL flag (also stored) → stored value → `navigator.language` starting with `zh` ⇒ `zh-HK`, otherwise `en`.
- `addStrings(table)` / `i18n.add(table)` — `{ key: ['中文', 'English'] }` or `{ key: { 'zh-HK': '…', en: '…' } }`. Later calls override. Empty English falls back to Chinese.
- `t(key, params?, lang?)` — current language; `{name}` placeholders filled from `params`; unknown key ⇒ the key itself. `tBoth(key)` ⇒ `"中文 English"`.
- `getLang()`, `isZh()`, `setLang(lang, { persist = true })`, `toggleLang()`.
- `onLangChange(fn(lang))` ⇒ unsubscribe function. Also fires `window` event **`cyber:langchange`** (`e.detail.lang`). Use it to redraw dynamic text (HUD values, canvas textures, result screens).
- `applyI18n(root = document)` — called automatically on load, on every change and (v0.2.1) on the next microtask after any `addStrings()` once the DOM is ready, so tables registered by game modules paint without a manual call. Updates:
  - `[data-i18n="key"]` → `textContent` (optional `data-i18n-params='{"n":3}'`)
  - `[data-i18n-html="key"]` → `innerHTML` (trusted game strings only)
  - `[data-i18n-attr="title:key,aria-label:key2"]` → attributes
  - `.glitch[data-i18n]` → also mirrors the text into `data-text` (glitch layers) (v0.2.1)
  - `<title data-i18n="key">` → `document.title`; `<html lang>` (`zh-Hant-HK` / `en`) and `<html data-lang="zh|en">` for CSS.
- `bindToggle(button, { onToggle })` — turns a button into the language switch (shows `EN` while Chinese is active, `中` while English is active; class `.lang-btn`, `[data-lang-toggle]`).
- Kit strings live under `kit.*` (`kit.paused`, `kit.watchAd`, `kit.noThanks`, `kit.endless`, `kit.bestEndless`, `kit.privacy`, `kit.demo`, …); `CyberUI.confirm` defaults use them. Legacy `STR`/`t2` remain exported for old code.
- `i18n` object bundles everything: `i18n.t / add / lang / set / toggle / onChange / apply / bindToggle`.
- `themeLabel(theme)` (core/theme.js) returns the district name in the current language.
- CSS (hud.css): `.lang-btn`, `.lang-corner` (fixed top-right helper), and `html[data-lang="en"]` typography tweaks for `.title/.title2/.banner-main/.neon-btn`.

```js
import { i18n, t } from 'cyber-kit';
i18n.add({ 'g.title': ['數據熔合', 'DATA FUSE'], 'g.level': ['第 {n} 關', 'LEVEL {n}'] });
i18n.bindToggle(document.getElementById('btn-lang'));
i18n.onChange(() => renderHud());          // dynamic strings
ui.banner(t('g.level', { n: 12 }));
```

## core/endless.js (v0.2.0) — endless mode helpers
Every CYBER game must have an endless mode (no final "beat the game" state).
- `endlessCurve(n, { start = 0, cap = 1, tau = 12 })` — `start + (cap − start)·(1 − e^(−n/τ))`: rises smoothly and saturates at `cap` so difficulty stays playable forever.
- `milestoneOf(n, every = 10)` — milestone index when `n` is a multiple of `every` (else 0) — use for theme shifts / rewards / natural ad breaks.

## core/storage.js
`createStore(gameId)` → `{ get(k, def), set(k, v), getNum, setNum, getBool, setBool, getJSON, setJSON, remove(k), best, submitBest(score) → bool, clear() }`. Keys are `cyber.<gameId>.<key>`. Falls back to memory if localStorage is blocked.

## core/theme.js
- `U` — shared uniforms: `uTime, uC1, uC2, uC3, uFogColor, uFogDensity, uHorizon, uZenith, uGrid…` (used by backdrop + game shaders).
- `THEMES` — 6 HK districts `{ name, en, c1, c2, c3, fog, horizon, zenith, accent, grid }`.
- `themeFor(level)` cycles THEMES.
- `new ThemeController({ speed = 2.2, css = true })` → `.set(themeOrLevel, instant)`, `.update(dt)` (lerps uniforms), `.accent` (Color), `.current`. Sets CSS vars `--c1 --c2 --c3`.

## core/renderer.js
`createStage({ canvas, bloom = .85, bloomRadius = .45, bloomThreshold = .82, fov = 50, near, far, toneMapping = 'neutral', exposure = 1, maxPixelRatio = 2, onFatal })` →
`{ renderer, scene, camera, composer, bloomPass, cyberPass, bloomBase, flags, pixelRatio, width, height, fps, onResize(fn(w,h,pr)), resize(), setPixelRatio(pr), toScreen(vec3) → {x,y} CSS px, render(dt), loop(fn(dt, t, rawDt), { isActive, fpsEl }) }`.
Auto-quality lowers the pixel ratio when FPS stays low while `isActive()` is true.

## core/post.js
`CyberShader` — ShaderPass material with `uTime, uAberration, uGlitch, uVignette, uGrain, uFlash`.

## core/fx.js
- `new Particles(scene, max = 2500, { floorY })` — `.emit(p, v, color, opts)`, `.burst(center, color, count, { speed, up, life, size, grav, spread, color2, bright })`, `.ring(center, color, count, speed, y)`, `.update(dt)`, `.resize(h, pr)`.
- `new Shockwaves(scene, n = 8)` — `.spawn(pos, color, { r0, r1, h, dur, a })`, `.update(dt)`.
- `new FxState()` — fields `trauma, aberr, glitch, fovKick, slowmo, danger`; `.kick({...})`, `.update(dt)`, `.timeScale`, `.shake(camera, t, amount)` (call after lookAt), `.applyPost(stage, t)`.

## core/backdrop.js
`new NeonCity(stage, { floor: 'reflect'|'plain'|'none', floorHalf, arena, innerRadius = 27, buildings = 300, billboard: { zh, en, pos, width }, signs, rain, dust, traffic, quality, dustArea, dustHeight })`
→ `.pulse(x, z, strength, delay)`, `.setLight('A'|'B', x, z, color, radius)`, `.danger = 0..1`, `.update(t, dt, camera)`. Also exports `NOISE_GLSL`, `FOG_GLSL` chunks.

## audio/synth.js
`new SynthAudio({ store, music: 'drive'|'chill'|preset, volume })` — call `.init()` from a user gesture (it refuses to create an AudioContext before the first gesture).
`.setMuted(b)`, `.toggleMute()` (persisted as `muted`), `.duckAll(on)` (ads), `.osc({...})`, `.noiseHit({...})`, SFX `click confirm back denied tick whoosh levelUp fail chime(n)`, music `startMusic stopMusic duckMusic unduckMusic setLevel(l)`. `mtof(midi)`, `MUSIC` presets. Suspends while the page is hidden.

## input/input.js
`createInput({ dir(d, info), tap(p), holdStart(p), holdEnd(p), action(name), anyGesture() }, { target, swipe: 'once'|'chain', threshold = 24, holdMs = 380, tapMaxMove = 14, keys, actions, ignore })` → `{ setEnabled(b), dispose() }`.
Default actions: Enter/Space `primary`, P/Esc `pause`, M `mute`, Z/U/Backspace `undo`, R `restart`, C `camera`, F `fps`. Pointer events on buttons/links/`[data-no-input]` are ignored.

## ui/ui.js + ui/hud.css
`new CyberUI({ screens: ['start','pause','over'] })` (elements `#screen-<name>`) → `.show(name|null)`, `.hud(on)`, `.loaded()`, `.fatal(msg)`, `.on(id, fn)`, `.setText(id, v)`, `.bump(el)`, `.setMuted(b)`, `.popup(x, y, text, sub, cls)`, `.banner(main, sub, note)` + `.tick(dt)`, `.flash(color, ms)`, `.toast(text, ms)`, `.confirm({ kicker, title, text, ok, okSmall, cancel, cancelSmall }) → Promise<bool>`, `.modalOpen`, `.closeModal()`.
CSS building blocks: `.hud-panel .stat .label .value .level-progress .lp-* .icon-btn .neon-btn(.ghost) .screen(.hero) .panel(.small) .title .title2 .glitch .results .ck-toast .ck-modal`.

## ui/strings.js
`STR` zh-HK/EN pairs (`[zh, en]`), `t2(key)` → "zh EN".

## platform/platform.js
`Platform.isNative`, `.name`, `.plugin(name)`, `.onBack(fn → true if handled)` (newest first; unhandled → minimise app), `.onPause(fn)`, `.onResume(fn)`, `.haptic('light'|'medium'|'heavy'|'success'|'warning'|'error')`, `.setHaptics(b)`, `.exit()`, `.openUrl(url)`.

## platform/ads.js
`createAds({ gameId, units: { android: { interstitial, rewarded } }, testing = true, interstitialCooldownSec = 180, breaksBetweenInterstitials = 3, graceSec = 120, webReward = 'grant', onAdOpen(on), maxAdContentRating = 'ParentalGuidance' })` →
`.init()` (AdMob.initialize + UMP consent), `.privacyOptionsRequired`, `.showPrivacyOptions()`, `.canShowInterstitial()`, `.naturalBreak(placement) → Promise<bool>` (call from Retry/Next handlers only), `.rewardedAvailable()`, `.rewarded(placement) → Promise<{ rewarded, reason }>`, `.state`, `.isNative`.
Web build never loads ads; `?adsim=1` shows a simulated overlay. `TEST_UNITS` = Google's public test ids.
Policy: never show interstitials at launch, exit or level start; rewarded ads must be opt-in.
