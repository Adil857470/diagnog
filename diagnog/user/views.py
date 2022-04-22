from django.shortcuts import render
from user.models import *
from django.contrib.auth import get_user_model
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
# from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, redirect
# Create your views here.


def index(request):
    return render(request, 'index/index.html')


def signIn(request):
    return render(request, 'user/signin.html')


def signUp(request):
    return render(request, 'user/signup.html')


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
        email = request.POST.get('email', None)
        if User.objects.filter(email=email).exists() == False:
            email = request.POST.get('email')
            if request.POST['password'] == request.POST['confirm_password']:
                user = User(username=email, email=email,
                            password=request.POST.get('password'))
                user.is_active = False
                user.save()
                phone = request.POST['phone']
                Profile.objects.create(username=user, phone=phone)
                # current_site = get_current_site(request)
                # mail_subject = 'Activate your Seeker account.'
                # message = render_to_string('email/email_template.html', {
                #     'user': user,
                #     'domain': current_site.domain,
                #     'uid': urlsafe_base64_encode(force_bytes(user.id)),
                #     'token': account_activation_token.make_token(user),
                # })
                # to_email = email
                # # send_mail(mail_subject, message, 'youremail', [to_email])
                # msg = EmailMultiAlternatives(
                #     mail_subject, message, 'youremail', [to_email])
                # msg.attach_alternative(message, "text/html")
                # msg.send()
            else:
                return render(request, 'user/signup.html', {"message": "Password not matched."})
            return render(request, 'user/signin.html')
        else:
            return render(request, 'user/signup.html', {"message": "User already exist."})

    return render(request, 'user/signup.html')
