from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

import stripe

from subscriptions.models import StripeCustomer
from checkout.models import Order
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    """ Display the user's profile. """
    try:

        profile_data = get_object_or_404(UserProfile, user=request.user)
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = (stripe.Subscription.
                        retrieve(stripe_customer.stripeSubscriptionId))
        product = stripe.Product.retrieve(subscription.plan.product)

        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=profile_data)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully')
            else:
                messages.error(request,
                               'Update failed.'
                               'Please ensure the form is valid.')
        else:
            form = UserProfileForm(instance=profile_data)
        orders = profile_data.orders.all()

        template = 'profiles/profile.html'
        context = {
            'form': form,
            'orders': orders,
            'on_profile_page': True,
            'subscription': subscription,
            'product': product,
        }

        return render(request, template, context)

    except StripeCustomer.DoesNotExist:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=profile_data)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully')
            else:
                messages.error(request,
                               'Update failed.'
                               'Please ensure the form is valid.')
        else:
            form = UserProfileForm(instance=profile_data)
        orders = profile_data.orders.all()

        template = 'profiles/profile.html'
        context = {
            'form': form,
            'orders': orders,
            'on_profile_page': True,
        }

        return render(request, template, context)


def order_history(request, order_number):
    """
    A view to display the order history
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


def unsubscripe(request):
    """
    A view to unsubscripe customers
    """
    stripe_customer = StripeCustomer.objects.get(user=request.user)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    stripe.Subscription.delete(
        stripe_customer.stripeSubscriptionId,
    )
    stripe_customer.delete()
    messages.success(request, 'You have succesfully unsubscriped!')

    return redirect(reverse('subscription_page'))
