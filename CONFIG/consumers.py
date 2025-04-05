import json
import os

from channels.generic.websocket import AsyncWebsocketConsumer


class CeleryLogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 建立 WebSocket 連接時，加入 'celery_logs' 群組
        await self.channel_layer.group_add("celery_logs", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # 斷開連接時，從群組中移除
        await self.channel_layer.group_discard("celery_logs", self.channel_name)

    async def log_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))


print(f"{os.path.relpath(__file__)}：我被讀取")
