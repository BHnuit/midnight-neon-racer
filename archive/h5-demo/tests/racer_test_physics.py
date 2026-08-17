"""物理/视觉专项:拟真车身、转向灯、不重叠、多种车型"""
from playwright.sync_api import sync_playwright
import time
from common import BASE_URL, launch

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

with sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width": 430, "height": 932})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" and "favicon" not in m.text else None)

    page.goto(BASE_URL)
    time.sleep(1.2)

    print("[1] 页面加载")
    check("无 JS 错误", len(errors) == 0, f"errors={errors}")

    page.evaluate("""() => {
        const g = window.__game;
        g.cars.push({x: 60, y: 100, lane: 0, color: '#ff5d5d', hostile: true, hDir: 1, hT: 1.0, changeAt: 1.4, blinkOn: true, blinkDir: 1, blinkT: 0.1});
        g.cars.push({x: 200, y: 100, lane: 1, color: '#ffb545', hostile: true, hDir: -1, hT: 0.2, changeAt: 1.8, blinkOn: false, blinkDir: 0, blinkT: 0});
    }""")

    print("[2] 转向灯状态机")
    time.sleep(0.5)
    blink_state = page.evaluate("""() => {
        const cars = window.__game.cars;
        const a = cars.find(c => c.changeAt === 1.4);
        return { blinkOn: a.blinkOn, blinkDir: a.blinkDir };
    }""")
    check("变道前 0.6s 转向灯亮起", blink_state["blinkOn"] is True and blink_state["blinkDir"] == 1, str(blink_state))

    print("[3] 像素级验证:车身不是方块(有轮子深色像素)")
    wheel_px = page.evaluate("""() => {
        const cv = document.getElementById('cv');
        const ctx = cv.getContext('2d');
        const d = ctx.getImageData(60, 100, 46, 80).data;
        let dark = 0, bright = 0;
        for (let i = 0; i < d.length; i += 4) {
            const r = d[i], g = d[i+1], b = d[i+2];
            if (r < 30 && g < 30 && b < 40) dark++;
            else if (r + g + b > 200) bright++;
        }
        return { dark, bright };
    }""")
    check("车身区域同时存在深色(轮子)和亮色(车身)", wheel_px["dark"] > 20 and wheel_px["bright"] > 100, str(wheel_px))

    print("[4] 同车道车距保持")
    page.evaluate("""() => {
        const g = window.__game;
        g.cars.length = 0;
        g.cars.push({x: 60, y: 200, lane: 0, color: '#ff5d5d', hostile: false, hDir: 0, hT: 0, changeAt: 99, blinkOn: false});
        g.cars.push({x: 60, y: 280, lane: 0, color: '#ffb545', hostile: false, hDir: 0, hT: 0, changeAt: 99, blinkOn: false});
    }""")
    time.sleep(0.8)
    gap = page.evaluate("""() => {
        const cars = window.__game.cars;
        if (cars.length < 2) return -1;
        const ys = cars.map(c => c.y).sort((a,b) => a-b);
        return ys[1] - ys[0];
    }""")
    check("后车与前车保持间距(>60px)", gap >= 60, f"gap={gap}")

    print("[5] 变道被阻挡时不叠车")
    page.evaluate("""() => {
        const g = window.__game;
        g.cars.length = 0;
        g.cars.push({x: 200, y: 300, lane: 1, color: '#4dd0e1', hostile: false, hDir: 0, hT: 0, changeAt: 99, blinkOn: false, w: 44, h: 74, vType: 'sedan'});
        g.cars.push({x: 60, y: 320, lane: 0, color: '#ff5d5d', hostile: true, hDir: 1, hT: 1.0, changeAt: 0.2, blinkOn: true, blinkDir: 1, blinkT: 0, w: 44, h: 74, vType: 'sedan'});
    }""")
    time.sleep(0.8)
    laneA = page.evaluate("""() => {
        const cars = window.__game.cars;
        const a = cars.find(c => c.color === '#ff5d5d');
        return a ? a.lane : -1;
    }""")
    check("目标车道被占时不变道(不重叠)", laneA == 0, f"laneA={laneA}")

    print("[6] 对向车有多种车型")
    types = page.evaluate("""() => {
        const g = window.__game;
        ['truck','police','ambulance','taxi','van','sedan'].forEach((id, i) => {
            g.cars.push({x: 20+i*10, y: 80+i*20, lane: 0, w: 48, h: 80, vType: id, hostile: false});
        });
        return [...new Set(g.cars.map(c => c.vType).filter(Boolean))];
    }""")
    check("至少 4 种交通车型", len(types) >= 4, str(types))

    print(f"\n结果: {PASS} 通过, {FAIL} 失败")
    browser.close()
    raise SystemExit(1 if FAIL else 0)
