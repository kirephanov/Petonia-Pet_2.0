from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', index, name='home'),
    path('map/', cache_page(60)(map_page), name='map'),
    path('add_post/', form_page, name='form'),
    path('post/', bulletin_page, name='board'),
    path('post/region/<int:region_id>/', get_region, name='region'),
    path('post/category/<int:category_id>/', get_category, name='category'),
    path('post/animal/<int:animal_id>/', get_animal, name='animal'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('post/<int:pk>/', GetPost.as_view(), name='post'),
    path('post/popular/', get_popular, name='popular'),
    path('authorization/', mobileLogin_page, name='mobile-login'),
    path('profile/', mobileLogout_page, name='profile'),
]