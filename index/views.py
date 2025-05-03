from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime

import json


def index(request):
    return render(request, "index/index.html")
