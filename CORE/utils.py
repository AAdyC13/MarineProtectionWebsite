import os
import trafilatura
from .models import cleanText as ct
# from asgiref.sync import async_to_sync

# import channels.layers
# channel_layer = channels.layers.get_channel_layer()

folder_path = "C:\\Users\\AAdy\\Desktop\\開發環境\\海洋保護宣傳網站\\語料庫"


def dataLoadIn():
    for filename in os.listdir(folder_path):
        if filename.endswith('.html') or filename.endswith('.htm'):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()

            # 用 trafilatura 抽取正文
            extracted_text = trafilatura.extract(html)

            if extracted_text:
                print(f'✔ 已讀取：{filename}')
            else:
                print(f'✘ 無法擷取正文：{filename}')


dataLoadIn()
