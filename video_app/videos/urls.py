from django.urls import path
from .views import (
    VideoRetrieveView, VideoListView, VideoIDsView,
    LikeToggleView, StatisticsSubqueryView, StatisticsGroupByView
)

urlpatterns = [
    path('v1/videos/<int:pk>/', VideoRetrieveView.as_view(), name='video-detail'),
    path('v1/videos/', VideoListView.as_view(), name='video-list'),
    path('v1/videos/<int:video_id>/likes/', LikeToggleView.as_view(), name='video-likes'),
    path('v1/videos/ids', VideoIDsView.as_view(), name='video-ids'),
    path('v1/videos/statistics-subquery', StatisticsSubqueryView.as_view(), name='stats-subquery'),
    path('v1/videos/statistics-group-by', StatisticsGroupByView.as_view(), name='stats-group-by')
]


