from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMultiAlternatives
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import F, Q
from datetime import datetime
from django.http import FileResponse


def index(request):
    return render(request, 'index/index.html')


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def signUp(request):
    User = get_user_model()

    if request.method == 'POST':

        if request.POST.get('password') != request.POST.get('confirm_password'):
            return render(request, 'user/signup.html', {"data": 'Please confirm your passwords'})

        email = request.POST.get('email', None)
        if User.objects.filter(email=email).count() == 0:
            email = request.POST.get('email')
            user = User(username=email, email=email,
                        password=request.POST.get('password'))
            user.is_active = False
            user.save()
            Profile.objects.create(user=user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('email/email_template.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email

            msg = EmailMultiAlternatives(
                mail_subject, message, to_email, [to_email])
            msg.attach_alternative(message, "text/html")
            msg.send()
            return render(request, 'user/signup.html', {"data": 'Please confirm your email address to complete the registration !'})
        else:
            return render(request, 'user/signup.html', {"data": 'Email Already Registered !'})

    return render(request, 'user/signup.html')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(signIn)
    else:
        print(account_activation_token.check_token(user, token))
        return HttpResponse('<h2>Activation link Expired!</h2>')


def userprofile(request):
    return render(request, 'user/profile.html')


def signIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.filter(username=email).first()
            if user.password == password:
                status = True
            else:
                status = False
            print(status)

            if not user.is_active:
                return render(request, 'user/signin.html', {'data': 'Please verify you email !'})

            if user.is_superuser:
                return redirect('Admin')

            if status and user.is_active:

                auth.login(request, user)
                request.session['username'] = email
                return redirect('index')
            else:
                return render(request, 'user/signin.html', {'data': 'Invalid Credentials'})

        except Exception as e:
            print(e)
            return redirect('signIn')
    return render(request, 'user/signin.html')


def logout(request):

    uid = User.objects.get(username=request.user)
    auth.logout(request)

    if request.session.has_key('username'):
        del request.session['username']
    else:
        pass

    return redirect('signIn')
