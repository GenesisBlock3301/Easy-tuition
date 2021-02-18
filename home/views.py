from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import User
from django.urls import reverse
from django.views import View
from django.core.mail import send_mail
from TuitionManagement.settings import EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.http import HttpResponse
from users.tokens import account_activation_token


def register(request):
    user_type = request.POST['user_type']
    full_name = request.POST['full_name']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    # password = None
    # print(">>>>>>>>>>>>>>>>>>>>", password1, password2)
    if password1 == password2:
        user = User.objects.filter(email=email)
        if user_type == 'client':
            if not user.exists():
                user = User.objects.create_user(full_name, email, 'client', password1)
                if user is None:
                    messages.error(request, 'Cannot create account, try again later')
                else:
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your account.'
                    message = render_to_string('account-active.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.id)),
                        'token': account_activation_token.make_token(user),
                    })
                    # print("Message----------------link",message,email,EMAIL_HOST_USER)
                    e = EmailMessage(
                        mail_subject, message, to=[email]
                    )
                    e.send()
                    messages.success(request, 'Please Check Your Email')
                    return redirect('client-home')
            else:
                messages.error(request, 'Account already exists, try with a different email.')
                return redirect('{}#signup_client'.format(reverse('home-page')))
        # -----------------------------
        elif user_type == 'tutor':
            if not user.exists():
                user = User.objects.create_user(full_name, email, 'tutor', password1)
                if user is None:
                    messages.error(request, 'Cannot create account, try again later')
                else:
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your account.'
                    message = render_to_string('account-active.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.id)),
                        'token': account_activation_token.make_token(user),
                    })
                    # print("Message----------------link",message,email,EMAIL_HOST_USER)
                    e = EmailMessage(
                        mail_subject, message, to=[email]
                    )
                    e.send()
                    messages.success(request, 'Pleas cheak your email')
                    return redirect('tutor-home')
            else:
                messages.error(request, 'Account already exists, try with a different email.')
                return redirect(f"{reverse('home-page')}#signup_tutor")
        else:
            messages.error(request, 'Invalid user type.')

        return redirect('home-page')
    else:
        messages.error(request, "Password not match")
        return redirect('home-page')


class Home(View):
    def get(self, request):
        try:
            if request.user.is_client and request.user.is_authenticated:
                return redirect('client-home')
            elif request.user.is_tutor and request.user.is_authenticated:
                return redirect('tutor-home')
        except:
            return render(request, 'home/home.html')
        return render(request, 'home/home.html')

    def post(self, request):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        container = name + "\n" + email + "\n" + subject + "\n" + message
        print(container)
        # print('>>>>>>>>>>>>>>>>',name,">>>>>>>>>>>>",message,'>>>>>>>>>>>',email)
        send_mail(subject=subject, message=container, from_email=email, recipient_list=[EMAIL_HOST_USER],
                  fail_silently=False)

        return redirect('home-page')


def login(request):
    current_tab = request.GET.get('tab', 'client')
    email = request.GET.get('email', '')
    context = {
        'logged_in': False,
        'is_client': False,
        'is_tutor': False,
        'email': email,
        'current_tab': current_tab,
        'tutor_tab': 'show' if current_tab == 'tutor' else '',
        'client_tab': 'show' if current_tab == 'client' else '',
    }
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        context['logged_in'] = True
        context['is_client'] = user.is_client
        context['is_tutor'] = user.is_tutor
        return render(request, 'home/login.html', context=context)
    else:
        return render(request, 'home/login.html', context=context)
