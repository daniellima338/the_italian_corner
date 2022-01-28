from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import stripe

from subscriptions.models import StripeCustomer


@login_required
def subscription_page(request):
    """ A view to return the index page"""
    try:
        # Retrieve the subscription & product
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = (stripe.Subscription.
                        retrieve(stripe_customer.stripeSubscriptionId))
        product = stripe.Product.retrieve(subscription.plan.product)

        return render(request, 'subscriptions/subscription_page.html', {
            'subscription': subscription,
            'product': product,
        })

    except StripeCustomer.DoesNotExist:
        return render(request, 'subscriptions/subscription_page.html')


@csrf_exempt
def stripe_config(request):
    """ A function to get stripe key"""
    if request.method == 'GET':
        stripe_configuration = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_configuration, safe=False)

# taken from https://testdriven.io/blog/django-stripe-subscriptions/
@csrf_exempt
def create_checkout_session(request):
    """ A function to create the checkout session for the subscription"""
    if request.method == 'GET':
        domain_url = 'https://the-italian-corner.herokuapp.com/subscriptions/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=(request.user.id if
                                     request.user.is_authenticated else None),
                success_url=domain_url +
                'success?session_id={CHECKOUT_SESSION_ID}',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required
def success(request):
    """ A view to return the success page"""

    return render(request, 'subscriptions/success.html')


@csrf_exempt
def stripe_webhook(request):
    """ A function to get stripe webhooks"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WH_SECRET_SUBSCRIPTION
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        StripeCustomer.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
        )
        user = client_reference_id.save()
        print(user.username + ' just subscribed.')

    return HttpResponse(status=200)
