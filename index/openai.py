import json
import openai


seeds = [["SDGs 海洋プラスチック問題", "海の持続可能性 SDGs", "海洋の持続可能性", "海洋保全", "漁業資源", "生態系の生息地破壊"],
         ["ブルーカーボン", "マイクロプラスチック", "持続可能な漁業",
             "海洋プラスチックごみ", "海洋保護区（MPA）", "海洋生物多様性"],
         ["暖化", "海平面", "海水", "海洋", "環保"],
         ["垃圾", "海平面", "海水", "海洋", "環保"],
         ["海洋教育の普及", "海洋汚染", "海洋清掃", "海洋環境モニタリング", "海洋生態系", "海洋資源"],
         ["塑膠", "廢棄", "微粒", "污染", "海域"],
         ["升溫", "海洋酸化", "熱浪", "生態", "白化"],
         ["保育", "棲地", "永續", "漁業", "禁捕"],
         ["塑膠", "海域", "漁網", "漂流", "纏繞"]]
default_prompt = "用戶偏好使用繁體中文對話。你的回答必須在300字以內。\n你是一位專注於研究『永續發展目標（Sustainable Development Goals, SDGs）』的第十四項目標：「保育及永續利用海洋生態系，以確保生物多樣性並防止海洋環境劣化」的小老師。請對用戶自稱「海洋保護小講堂的小老師」。\n現在請根據以下「語料庫議題」與使用者交談，禁止主動提起其他議題。如果使用者問起請「語料庫議題」相關內容，你可以回答。\n注意，你的回答應該是專業且具體的，並且能夠幫助使用者更好地理解 SDGs 14 議題。\n\n「語料庫議題」：\n" + \
    str(seeds)


class OpenAIClient:
    def __init__(self, keys_path="keys.json"):
        # 從 keys.json 讀取 API 金鑰
        with open(keys_path, "r") as file:
            keys = json.load(file)
        self.api_key = keys.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found in keys.json")
        openai.api_key = self.api_key

    def send_prompt(self, sentence: str, history: list, model="o4-mini-2025-04-16", max_tokens=2000) -> str:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": default_prompt},
                # 加入歷史紀錄
                *[
                    {"role": "user", "content": item} if i % 2 == 0 else {
                        "role": "assistant", "content": item}
                    for i, item in enumerate(history)
                ],
                {"role": "user", "content": sentence}
            ],
            max_completion_tokens=max_tokens
        )
        text = response.choices[0].message.content.strip()
        return text


OpenAI = OpenAIClient()
