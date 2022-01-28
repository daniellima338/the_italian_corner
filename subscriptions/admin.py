from django.contrib import admin
from subscriptions.models import StripeCustomer, MonthlyWine


admin.site.register(StripeCustomer)

admin.site.register(MonthlyWine)
