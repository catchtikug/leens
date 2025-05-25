from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('logout/', views.logout_view, name='logout'),  # Add this line
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('report/side-effect/', views.submit_side_effect, name='side_effect'),
    path('report/drug-resistance/', views.submit_drug_resistance, name='drug_resistance'),
]
