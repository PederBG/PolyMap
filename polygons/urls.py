from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('save', views.save, name='save'),
    path('upload', views.upload, name='upload'),
    path('union/<str:ids>', views.union, name='union'),
    path('intersect/<str:ids>', views.intersect, name='intersect'),
]
