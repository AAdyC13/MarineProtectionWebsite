from django.urls import path
from index import views

urlpatterns = [
    path('', views.index, name='index.html'),
    # path("api/get_news_DBinfo/", views.get_news_DBinfo, name="get_news_DBinfo"),
]
