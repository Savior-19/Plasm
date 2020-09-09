from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.HomePage, name='home-page'),

    path('donor-search/', views.DonorSearch, name='donor-search'),

    # Registration Based Links

    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), {'template_name': 'home.html'}, name='logout'),
]
