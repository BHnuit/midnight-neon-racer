"""v5: 擦车连击、氮气、车手感、赛博像素、如祜彩蛋"""
from playwright.sync_api import sync_playwright
import time
from common import BASE_URL, launch, attach_errors

PASS = 0
FAIL = 0

def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✓ {name}")
    else:
        FAIL += 1
        print(f"  ✗ {name} {detail}")

def swipe(page, x0, y0, x1, y1):
    page.mouse.move(x0, y0)
    page.mouse.down()
    page.mouse.move(x1, y1, steps=8)
    page.mouse.up()

with sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width": 375, "height": 812})
    errors = attach_errors(page)

    page.goto(BASE_URL)
    time.sleep(1.0)

    print("[1] 图例 / 像素 CTA / 375 HUD")
    check("无 JS 错误", len(errors) == 0, f"errors={errors}")
    legend = page.locator("#overlayLegend").inner_text()
    check("图例含擦过/连击", ("擦过" in legend or "连击" in legend), legend[:90])
    check("图例含氮气", "氮气" in legend, legend[:90])
    check("图例含滑动", "滑动" in legend, legend[:90])
    css = page.evaluate("""() => {
        const b = getComputedStyle(document.querySelector('#startBtn'));
        return { img: b.backgroundImage, col: b.backgroundColor };
    }""")
    check("CTA 不是粉紫渐变", "7fb0ff" not in css["img"] and "ff7ad9" not in css["img"] and "gradient" not in (css["img"] or "").lower(), str(css))

    score = page.locator("#scoreHud").bounding_box()
    mute = page.locator("#muteBtn").bounding_box()
    share = page.locator("#shareBtn").bounding_box()
    nitro = page.locator("#nitroWrap").bounding_box()
    check("静音/转发在 375 内", mute and share and mute["x"] >= 0 and share["x"] + share["width"] <= 376, f"mute={mute} share={share}")
    if score and mute:
        overlap = not (score["x"] + score["width"] < mute["x"] - 2 or mute["x"] + mute["width"] < score["x"] - 2)
        check("分数不与静音钮重叠", overlap is False, f"score={score} mute={mute}")
    check("氮气条在 375 内", bool(nitro) and nitro["x"] >= 0 and nitro["x"] + nitro["width"] <= 376, str(nitro))

    print("[2] 七车手感不同 + 疾风仍蓝")
    stats = page.evaluate("window.__game.carStats")
    check("7 辆车", isinstance(stats, list) and len(stats) == 7, str(stats))
    keys = ("grip", "accel", "topSpeed", "brake", "nitroEff", "slide")
    sigs = [tuple(round(c[k], 3) for k in keys) for c in stats]
    check("手感不全相同", len(set(sigs)) == 7, str(sigs))
    check("疾风仍蓝", "7fb0ff" in (stats[0].get("color") or "").lower() or "9cc4ff" in (stats[0].get("color") or "").lower(), str(stats[0]))
    check("烈焰更快更滑", stats[1]["topSpeed"] > stats[0]["topSpeed"] and stats[1]["slide"] > stats[0]["slide"] and stats[1]["brake"] < stats[0]["brake"], str(stats[1]))

    print("[3] 发车后擦车连击与氮气")
    page.click("#startBtn")
    time.sleep(0.4)
    check("overlay 隐藏", not page.locator("#overlay").is_visible())
    page.evaluate("window.__game.setNitro(0); window.__game.setCombo(0)")
    before = page.evaluate("({s: window.__game.score, n: window.__game.nitro, c: window.__game.combo})")
    page.evaluate("window.__game.forceNearMiss(10)")
    after = page.evaluate("({s: window.__game.score, n: window.__game.nitro, c: window.__game.combo, nm: window.__game.nearMiss})")
    check("擦车加分", after["s"] > before["s"], str(after))
    check("擦车加氮气", after["n"] > before["n"], str(after))
    check("擦车加连击", after["c"] >= 1, str(after))
    check("nearMiss 计数", after["nm"]["count"] >= 1, str(after["nm"]))

    page.evaluate("window.__game.setCombo(4)")
    time.sleep(2.4)
    decayed = page.evaluate("window.__game.combo")
    check("连击会衰减", decayed < 4, f"combo={decayed}")

    print("[4] 氮气才是加速,无氮气上滑不送极速")
    page.evaluate("window.__game.setNitro(0); window.__game.setSpeed(200)")
    box = page.locator("#cv").bounding_box()
    cx = box["x"] + box["width"] * 0.5
    cy = box["y"] + box["height"] * 0.55
    swipe(page, cx, cy, cx, cy - 90)
    time.sleep(0.4)
    dry = page.evaluate("window.__game.speed")
    check("无氮气上滑不暴涨", dry < 260, f"speed={dry}")
    page.evaluate("window.__game.setNitro(90); window.__game.setSpeed(200)")
    n0 = page.evaluate("window.__game.nitro")
    swipe(page, cx, cy, cx, cy - 90)
    time.sleep(0.4)
    wet = page.evaluate("({s: window.__game.speed, n: window.__game.nitro})")
    check("有氮气上滑加速", wet["s"] > 220, str(wet))
    check("上滑消耗氮气", wet["n"] < n0, f"{n0}->{wet['n']}")
    page.evaluate("window.__game.setSpeed(240)")
    swipe(page, cx, cy, cx, cy + 90)
    time.sleep(0.4)
    brk = page.evaluate("window.__game.speed")
    check("下滑刹车", brk < 230, f"speed={brk}")

    print("[5] 如祜出行 626 只刷一次")
    pre = page.evaluate("""() => {
        window.__game.setScore(625);
        return {
          s: window.__game.score,
          spawned: window.__game.ruqiSpawned,
          n: window.__game.cars.filter(c => c.ruqi || c.vType==='ruqi').length
        };
    }""")
    check("625 尚未刷出", pre["spawned"] is False and pre["n"] == 0 and pre["s"] < 626, str(pre))
    # 等分数自然越过 626,或直接推到 626
    deadline = time.time() + 3.0
    while time.time() < deadline:
        sc = page.evaluate("window.__game.score")
        if sc >= 626:
            break
        time.sleep(0.15)
    if page.evaluate("window.__game.score") < 626:
        page.evaluate("window.__game.setScore(626)")
    time.sleep(0.25)
    mid = page.evaluate("""() => {
        const rs = window.__game.cars.filter(c => c.ruqi || c.vType==='ruqi');
        const W = 400, LANE_W = W/3;
        const divs = [LANE_W, LANE_W*2];
        let onDiv = 0;
        for (const c of rs) {
          const cx = c.x + (c.w||46)/2;
          if (divs.some(d => Math.abs(cx - d) < 16)) onDiv++;
        }
        return { spawned: window.__game.ruqiSpawned, n: rs.length, onDiv, lanes: rs.map(c => c.lane) };
    }""")
    check("626 后恰好 1 辆如祜", mid["spawned"] is True and mid["n"] == 1, str(mid))
    check("如祜在车道里不在护栏线", mid["n"] == 0 or mid["onDiv"] == 0, str(mid))
    page.evaluate("""() => {
        const r = window.__game.cars.find(c => c.ruqi || c.vType==='ruqi');
        if (r) r.y = 432;
    }""")
    time.sleep(0.12)
    liv = page.evaluate("""() => {
        const r = window.__game.cars.find(c => c.ruqi || c.vType==='ruqi');
        if (!r) return {ok:false};
        const box = window.__game.screenBox(r);
        const cv = document.getElementById('cv');
        const ctx = cv.getContext('2d');
        const x = Math.max(0, Math.min(cv.width-1, box.x|0));
        const y = Math.max(0, Math.min(cv.height-1, box.y|0));
        const w = Math.max(1, Math.min(cv.width-x, box.w|0));
        const h = Math.max(1, Math.min(cv.height-y, box.h|0));
        const d = ctx.getImageData(x, y, w, h).data;
        let white=0, teal=0, red=0, yellow=0;
        for (let i=0;i<d.length;i+=4) {
          const R=d[i], G=d[i+1], B=d[i+2];
          if (R>210 && G>200 && B>190) white++;
          else if (G>140 && B>140 && R<90) teal++;
          else if (R>170 && G<70 && B<80) red++;
          else if (R>210 && G>170 && B<100) yellow++;
        }
        return {ok:true, white, teal, red, yellow, box};
    }""")
    check("如祜涂装有白/青/红/黄", liv.get("ok") and liv["white"]>30 and liv["teal"]>8 and liv["red"]>8 and liv["yellow"]>2, str(liv))
    page.evaluate("window.__game.setScore(900); window.__game.spawnRuqi()")
    time.sleep(0.2)
    post = page.evaluate("window.__game.cars.filter(c => c.ruqi || c.vType==='ruqi').length")
    check("不会刷第二辆", post <= 1, f"n={post}")

    print("[6] 对手幻影仍遵守上限")
    page.evaluate("""() => {
        window.__game.setLeaderboard([
            {name: '幽灵阿明', score: 4000, carId: 0, ts: 1},
            {name: '幽灵小雅', score: 5000, carId: 1, ts: 2},
            {name: '幽灵老周', score: 6000, carId: 2, ts: 3},
            {name: '幽灵阿飞', score: 7000, carId: 3, ts: 4},
        ]);
    }""")
    # 重新发车会清场;这里只检查当前同屏仍 <= 3
    gcount = page.evaluate("window.__game.ghostCars.length")
    check("同屏幻影 <= 3", gcount <= 3, f"count={gcount}")

    print(f"\n结果: {PASS} 通过, {FAIL} 失败")
    browser.close()
    raise SystemExit(1 if FAIL else 0)
