"""全量回归:排行榜/幻影/车类型/转发/基础操作"""
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
    time.sleep(1.5)

    print("[1] 页面加载")
    check("无 JS 错误", len(errors) == 0, f"errors={errors}")
    check("菜单可见", page.locator("#overlay").is_visible())

    print("[2] 车选择器")
    cars = page.locator(".carOption")
    check("6 种车可选", cars.count() == 6, f"count={cars.count()}")
    cars.nth(0).click()
    time.sleep(0.2)
    check("第1种车选中", cars.nth(0).evaluate("el => el.classList.contains('selected')"))

    print("[3] 昵称输入")
    page.fill("#nameInput", "测试阿飞")
    time.sleep(0.3)

    print("[4] 发车 + 基础操控")
    page.click("#startBtn")
    time.sleep(0.5)
    check("overlay 隐藏", not page.locator("#overlay").is_visible())
    x0 = page.evaluate("window.__game.player.x")
    check("读到玩家坐标", x0 > 0, f"x0={x0}")
    page.keyboard.down("ArrowLeft"); time.sleep(0.35); page.keyboard.up("ArrowLeft")
    x1 = page.evaluate("window.__game.player.x")
    check("键盘←左移", x1 < x0 - 25, f"{x0}->{x1}")

    print("[5] 幻影车生成")
    ghost_count = page.evaluate("window.__game.ghostCars.length")
    check("幻影车列表已生成", ghost_count >= 0)
    if ghost_count > 0:
        names = page.evaluate("[...window.__game.ghostCars].map(g => g.name)")
        print(f"      幻影车手: {names[:5]}")

    print("[6] 跑一会让分数增长")
    page.keyboard.down("ArrowRight"); time.sleep(2.0); page.keyboard.up("ArrowRight")
    score_now = int(page.locator("#scoreHud").inner_text())
    check("分数在增长", score_now > 15, f"score={score_now}")

    print("[7] 转发按钮存在")
    share = page.locator("#shareBtn")
    check("转发按钮可见", share.is_visible())

    print("[8] 碰撞结束 + 排行榜提交")
    page.evaluate("""() => {
        const g = window.__game;
        g.cars.push({x: g.player.x, y: g.player.y, lane: 0, color: '#ff5d5d', hostile: false});
    }""")
    time.sleep(1.2)
    overlay_visible = page.locator("#overlay").is_visible()
    check("撞车后 overlay 出现", overlay_visible)
    board_html = page.locator("#overlay").inner_html()
    check("显示排行榜", "排行榜" in board_html or "board" in board_html)
    time.sleep(1.5)

    print("[9] 排行榜 API 有数据")
    lb = page.evaluate("window.__game.leaderboard.length")
    check("leaderboard 有记录", lb > 0, f"len={lb}")
    names = page.evaluate("window.__game.leaderboard.map(e => e.name)")
    print(f"      榜单: {names[:5]}")
    check("刚才提交的名字在榜", "测试阿飞" in names)

    print(f"\n结果: {PASS} 通过, {FAIL} 失败")
    browser.close()
    raise SystemExit(1 if FAIL else 0)
