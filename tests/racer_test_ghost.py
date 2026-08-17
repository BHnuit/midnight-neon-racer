"""幻影陪跑:同屏最多 3、不重叠、低分下场补位"""
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
    check("无 JS 错误", len(errors) == 0, f"errors={errors}")

    page.evaluate("""() => {
        window.__game.setLeaderboard([
            {name: '幽灵阿明', score: 400, carId: 0, ts: 1},
            {name: '幽灵小雅', score: 2000, carId: 1, ts: 2},
            {name: '幽灵老周', score: 1200, carId: 2, ts: 3},
            {name: '幽灵阿飞', score: 800, carId: 3, ts: 4},
            {name: '幽灵桃子', score: 2600, carId: 4, ts: 5},
        ]);
    }""")
    time.sleep(0.3)

    print("[1] 发车后幻影车起步同场")
    page.click("#startBtn")
    time.sleep(0.6)
    ghost_count = page.evaluate("window.__game.ghostCars.length")
    check("同屏幻影 <= 3", ghost_count <= 3, f"count={ghost_count}")
    check("同屏幻影 >= 1", ghost_count >= 1, f"count={ghost_count}")
    ghost_ys = page.evaluate("[...window.__game.ghostCars].map(g => Math.floor(g.y))")
    print(f"      起步位置: {ghost_ys}")
    check("幻影都在屏幕内同场", all(0 < y < 620 for y in ghost_ys), str(ghost_ys))
    names = page.evaluate("[...window.__game.ghostCars].map(g => g.name)")
    check("按昵称去重", len(set(names)) == len(names), str(names))

    print("[2] 不重叠")
    overlap = page.evaluate("""() => {
        const gs = window.__game.ghostCars;
        for (let i = 0; i < gs.length; i++) {
          for (let j = i+1; j < gs.length; j++) {
            const a = gs[i], b = gs[j];
            if (a.lane === b.lane && Math.abs(a.y - b.y) < 80) return true;
          }
        }
        return false;
    }""")
    check("幻影彼此不重叠", overlap is False)

    print("[3] 低分车消失后补位下一辆")
    page.evaluate("window.__game.setScore(401)")
    time.sleep(0.8)
    after = page.evaluate("[...window.__game.ghostCars].map(g => g.name + ':' + g.score)")
    print(f"      补位后: {after}")
    names2 = page.evaluate("[...window.__game.ghostCars].map(g => g.name)")
    check("阿明已下场", "幽灵阿明" not in names2, str(names2))
    check("仍不超过 3 辆", len(names2) <= 3, str(names2))
    check("补上了更高分段车手", any(x in names2 for x in ["幽灵小雅", "幽灵桃子", "幽灵老周", "幽灵阿飞"]), str(names2))

    page.evaluate("""() => {
        const g = window.__game;
        g.cars.push({x: g.player.x, y: g.player.y, lane: 0, color: '#ff5d5d', hostile: false});
    }""")
    time.sleep(1.0)
    check("撞车结束", page.locator("#overlay").is_visible())

    print(f"\n结果: {PASS} 通过, {FAIL} 失败")
    browser.close()
    raise SystemExit(1 if FAIL else 0)
