import os
import logging
import sys

from __future__ import absolute_import, unicode_literals
from celery import Celery

# 設定 Django 的 settings 模組
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CONFIG.settings")

# 設定 Celery 日誌輸出
logger = logging.getLogger("celery")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Celery("MPWeb")  # 創建 Celery 實例
app.config_from_object("django.conf:settings",
                       namespace="CELERY")  # 加載 Django 設定
# app.autodiscover_tasks(["core.tasks", "core.news_scraper"])


@app.task(bind=True)
def debug_task(self):
    print(f"任務: {self.request!r}")


print(f"{os.path.relpath(__file__)}：我被讀取")
