from django.urls import path, re_path
from .views import userprofile

app_name = 'userprofile'

urlpatterns = [
    path('<pk>', userprofile, name='userprofile'),
]