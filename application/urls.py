from django.urls import path
from .views import *


urlpatterns = [
    path('thread/', ThreadDetail.as_view()),
    path('message/', MessageViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('message/<int:pk>/status/', MessageStatus.as_view()),
    path('thread/list/', ThreadList.as_view()),
    path('thread/<int:pk>/', ThreadDetail.as_view())
]
