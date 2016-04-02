from django.conf.urls import url

from . import views

urlpatterns = [
   #url(r'^', views.search_flipkart, name='search_flipkart'),
   url(r'^get_text/', views.get_text, name='get_text')
]
