from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscription_page, name='subscription_page'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
]