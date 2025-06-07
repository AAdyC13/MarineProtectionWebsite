from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from .openai import OpenAI
import uuid
import json

client = []


def index(request):
    return render(request, "index/index.html")


@csrf_exempt
def ai_connection(request):
    """
    處理 AI 連線請求
    """
    if request.method == "POST":
        data = json.loads(request.body)
        password = data.get("password", "")
        if password != "海洋保護小講堂":
            return JsonResponse({"status": "error", "message": "You are not authorized to access this resource."}, status=403)
        if len(client) >= 5:
            return JsonResponse({"status": "error", "message": "Too many connections, please try again later."}, status=429)
        token = str(uuid.uuid4())
        client.append({"token": token, "times": 0})
        response = {
            "status": "success",
            "token": token,
        }
        return JsonResponse(response)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


@csrf_exempt
def ai_talk(request):
    """
    處理 AI 對話請求
    """
    if request.method == "POST":
        data = json.loads(request.body)
        token = data.get("token", False)

        # 檢查 token 是否有效
        token_valid = False
        client_idx = -1
        for idx, c in enumerate(client):
            if c['token'] == token:
                token_valid = True
                client_idx = idx
                break

        if not token_valid:
            return JsonResponse({"status": "error", "message": "Invalid or expired token."}, status=403)

        if client[client_idx]["times"] >= 1:
            client.pop(client_idx)
            return JsonResponse({"status": "error", "message": "You have reached the maximum number of requests. AUTO_RETRY"}, status=429)

        sentence = data.get("sentence", "")
        history = data.get("history", [])

        # 使用 OpenAI API 獲取 AI 回應
        try:
            ai_response = OpenAI.send_prompt(sentence, history)
            if not ai_response:
                ai_response = "抱歉，我無法理解您的問題。請嘗試使用其他方式表達您的問題。"
            response = {
                "status": "success",
                "message": ai_response,
            }
            client[client_idx]["times"] += 1
            return JsonResponse(response)
        except Exception as e:
            print(f"AI處理錯誤: {e}")
            return JsonResponse({"status": "error", "message": f"AI處理錯誤"}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)
