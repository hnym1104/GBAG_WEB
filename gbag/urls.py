from django.contrib import admin
from django.urls import path
import intro.views 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',intro.views.home,name="home"),
    path('introduction/',intro.views.introduction, name="introduction"),
    path('predict/',intro.views.predict,name="predict"),
    path('result/',intro.views.result,name="result"),
    
]
