from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('<slug:username>/', views.ProfileDetailView.as_view(), name='detail'),
    path("<str:username>/update",views.ProfileUpdateView.as_view(), name='update'),
]