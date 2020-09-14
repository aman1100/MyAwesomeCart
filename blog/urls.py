from django.contrib import admin
from django.urls import path ,include
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='blogHome'),
    path('LatestProducts/',views.latestProducts,name='latestProducts'),
    path('blogPosts/<int:id>',views.blogPosts,name='blogPosts')
]