import datetime
import json
import requests
import hashlib

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .tokens import account_activation_token
from .forms import CustomUserCreationForm, OrderForm
from .models import Order, User


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your EZResume account'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user), })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request,
                             "Verification email sent to {}. Please activate your account ".format(user.email))
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "You're account is now active! Please login with your credentials")
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


@csrf_exempt
def payment_notification(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        request_dict = json.loads(body_unicode)
        order_id = request_dict['order_id']
        status_code = request_dict['status_code']
        gross_amount = request_dict['gross_amount']
        serverkey = 'SB-Mid-server-ZTiZXa5L2pyYVdAUljABci8P'

        if (request_dict["transaction_status"] == "settlement" or request_dict["transaction_status"] == "capture") and request_dict["status_code"] == "200":
            signature_key_encoded = (order_id + status_code + gross_amount + serverkey).encode('utf-8')
            m = hashlib.sha512()
            m.update(signature_key_encoded)

            if m.hexdigest() == request_dict['signature_key']:
                order = Order.objects.get(pk=order_id)
                user = order.user
                if order.package == '7 day':
                    user.profile.sub_expires_on = timezone.now() + datetime.timedelta(days=7)
                elif order.package == '1 month':
                    user.profile.sub_expires_on = timezone.now() + datetime.timedelta(days=30)
                user.save()
                order.paid_status = True
                order.save()
                group = Group.objects.get(name='paying_user')
                group.user_set.add(user)
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=401)
        else:
            return HttpResponse(status=201)
    return redirect('home')


def payment_confirmed(request):
    messages.success(request, "Thank you for your purchase! You now have unlimited PDF exports!")
    return redirect('resumes:my-resumes')


def payment(request):
    user = request.user
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            url = 'https://app.sandbox.midtrans.com/snap/v1/transactions/'
            if '7-day' in request.POST:
                order = Order.objects.create(user=user, package='7 day', total=24000)
            elif '1-month' in request.POST:
                order = Order.objects.create(user=user, package='1 month', total=72000)

            order_id = str(order.id)
            order_total = order.total

            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }

            payload = {
                "transaction_details": {
                    "order_id": order_id,
                    "gross_amount": order_total
                },
                "item_details": {
                    "name": '{} package'.format(order.package),
                    "price": order.total,
                    "quantity": 1,
                },
                "customer_details": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                },
                "billing_address": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                },
            }

            snap_token = requests.post(url, auth=('SB-Mid-server-ZTiZXa5L2pyYVdAUljABci8P', ''),
                                       headers=headers, json=payload)
            response_dict = snap_token.json()
            redirect_url = response_dict['redirect_url']
            return redirect(redirect_url)
    else:
        form = OrderForm()
    return render(request, 'users/payment.html', {'form': form, 'user': user})
