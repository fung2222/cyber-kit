"""cyber-kit loudness meter (v0.3.0).

Usage (serve the folder that contains the kit and the games, e.g. `cd ~/src && python3 -m http.server 8000`):
  python3 tests/loudness.py http://127.0.0.1:8000 data-fuse:FuseAudio cyber-board:BoardAudio cyber-snake:AudioEngine:snake
Options: --kit /cyber-kit   use this kit checkout instead of each game's vendor/cyber-kit
         --json out.json    write full results (incl. per-SFX momentary peaks)
         --level 2          music level passed to setLevel()
Needs Playwright (pip install playwright) and Chrome/Chromium (CHROME=/path/to/chrome).
The meter page is loaded from <BASE>/<kit dir>/tests/loudness.html (default kit dir name: cyber-kit).
Targets (docs/API.md "Loudness"): music ≈ -20 LUFS integrated, SFX/BGM ratio 0 ± 2 dB.
"""
import asyncio, json, os, sys
from playwright.async_api import async_playwright

def main():
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(1)
    opts = {'--kit': '', '--json': '', '--level': '2', '--meter': '/cyber-kit/tests/loudness.html'}
    rest = []
    i = 0
    while i < len(a):
        if a[i] in opts: opts[a[i]] = a[i + 1]; i += 2
        else: rest.append(a[i]); i += 1
    base, games = rest[0].rstrip('/'), rest[1:]
    asyncio.run(run(base, games, opts))

async def run(base, games, opts):
    res = {}
    async with async_playwright() as p:
        kw = {'args': ['--autoplay-policy=no-user-gesture-required']}
        if os.environ.get('CHROME'): kw['executable_path'] = os.environ['CHROME']
        b = await p.chromium.launch(**kw)
        for g in games:
            parts = g.split(':'); d, cls = parts[0], parts[1]
            cfg = {'mod': f'/{d}/js/audio.js', 'cls': cls, 'snake': 'snake' in parts[2:], 'level': int(opts['--level'])}
            pg = await b.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            url = f"{base}{opts['--meter']}?dir={d}" + (f"&kit={opts['--kit']}" if opts['--kit'] else '')
            await pg.goto(url); await pg.wait_for_function('window.__ready')
            try: r = await pg.evaluate('c => measure(c)', cfg)
            except Exception as e: r = {'error': str(e)[:300]}
            r['pageErrors'] = errs[:3]; res[d] = r; await pg.close()
            if 'error' in r: print(f'{d:18s} ERROR {r["error"]}'); continue
            m = r['music']
            print(f"{d:18s} music {m['lufs']:6.1f} LUFS  rms {m['rms']:6.1f}  peak {m['peak']:5.1f} dBFS | sfx median {r['sfxMedianMomentary']:6.1f}  max {r['sfxMax']:6.1f} | sfx/bgm {r['ratio']:+.1f} dB")
        await b.close()
    if opts['--json']: json.dump(res, open(opts['--json'], 'w'), indent=1)

if __name__ == '__main__':
    main()
