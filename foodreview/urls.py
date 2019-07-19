from django.urls import path
from .views import *
from django.conf.urls import url

urlpatterns = [
    path('', index, name='index'),
    path('restlist/', RestListView.as_view(), name='rest'),
    path('restlist/<int:pk>', RestDetailView.as_view(), name='rest-detail'),
    path('regionlist/', RegionListView.as_view(), name='region'),
    path('regionlist/<int:pk>', RegionDetailView.as_view(), name='region-detail'),
    path('review/create', ReviewCreate.as_view(), name='review-create'),
    path('myreviews/', ReviewsByUser.as_view(), name='my-review'),
    path('allreviews/', ReviewsByAll.as_view(), name='all-review'),
    url(r'review/create/(?P<id>\d+)', post_detail, name="post_detail"),
]

