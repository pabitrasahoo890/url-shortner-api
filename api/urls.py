from django.urls import path
from . import views

urlpatterns = [
    path('api/shorten', views.shorten_url, name='shorten_url'),
    path('api/stats/<str:short_code>', views.get_stats, name='get_stats'),
    path('<str:short_code>', views.redirect_url, name='redirect_url'),
]
