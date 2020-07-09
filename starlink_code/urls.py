from django.urls import path
from starlink_code import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('download', views.download_file, name='df'),
]
