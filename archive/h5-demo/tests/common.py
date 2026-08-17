"""共享测试配置。默认打线上,可用环境变量覆盖。"""
import os

BASE_URL = os.environ.get("RACER_URL", "https://racer.bhnuit.cn/")
CHROME = os.environ.get("PLAYWRIGHT_CHROMIUM", "")


def launch(p):
    kwargs = {"headless": True}
    if CHROME:
        kwargs["executable_path"] = CHROME
    return p.chromium.launch(**kwargs)
