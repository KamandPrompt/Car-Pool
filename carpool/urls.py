from django.urls import path

from . import views


urlpatterns = [
    path('new/', views.new, name="new"),
    path('', views.dashboard, name="dashboard"),
    path('add/', views.addPool, name="addPool"),
    path('log/', views.log, name="log"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
