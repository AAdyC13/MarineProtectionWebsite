from django.urls import path
from index import views

urlpatterns = [
    path('', views.index, name='index.html'),
    path('api/ai_connection/', views.ai_connection, name='ai_connection'),
    path('api/ai_talk/', views.ai_talk, name='ai_talk'),
    # path("api/get_news_DBinfo/", views.get_news_DBinfo, name="get_news_DBinfo"),
]
