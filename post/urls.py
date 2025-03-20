from django.urls import path
from .views import HomeView,CreatePostView

app_name = 'post'

urlpatterns = [
    path('',HomeView.as_view(),name='index'),
    path('create/',CreatePostView.as_view(),name='create_post')
]
