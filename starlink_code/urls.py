from django.urls import path
from starlink_code import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('downloadfile', views.download_file, name='df'),
    path('downloadicon', views.download_icon, name='di'),
    path('downloadupdate', views.download_update, name='du'),
]
