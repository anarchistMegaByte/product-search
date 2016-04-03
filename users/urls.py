from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/', views.register_and_tokenize, name='user registration'),
    #url(r'^login/', views.user_to_login, name='user login'),
    #url(r'^logout/', views.user_to_logout, name='user logout'),
]