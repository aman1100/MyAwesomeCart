from django.contrib import admin
from django.urls import path ,include
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='shopHome'),
    path('about/',views.about,name='AboutUs'),
    path('contactus/',views.contactus,name='ContactUS'),
    path('tracker/',views.tracker,name='tracker'),
    path('search/',views.search,name='search'),
    path('productview/<int:myid>',views.productview,name='productview'),
    path('checkout/',views.checkout,name='checkout'),
    path('handlerequest/',views.handlerequest,name='HandleRequest')
]