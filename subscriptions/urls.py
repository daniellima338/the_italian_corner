from django.urls import path
from . import views
from .views import stripe_webhook

urlpatterns = [
    path('', views.subscription_page, name='subscription_page'),
    path('create-checkout-session/', views.create_checkout_session),
    path('config/', views.stripe_config),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
]
