from django.urls import path
from . import views
app_name = "food"
urlpatterns = [
   path('',views.home, name="home"),
   path('menu/',views.menu, name="menu"),
]