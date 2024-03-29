from django.urls import path
from starlink_code import views, functions

urlpatterns = [
    path('', views.index, name='index'),
    #path('test', views.test, name='ts'),
    #path('form', views.get_form, name='gf'),
    path('downloadfile', views.download_file, name='df'),
    path('downloadicon', views.download_icon, name='di'),
    path('downloadupdate', views.download_update, name='du'),
]

functions.networkLink("networklink.kml",65)
functions.updateStarLink()
