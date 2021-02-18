from django.shortcuts import render, HttpResponse
from django.views import View
from django.core.mail import send_mail
from TuitionManagement.settings import EMAIL_HOST_USER
from .models import User
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib import messages

class ContactView(View):
    def get(self, request):
        return render(request, 'app/site/contact.html')

    def post(self, request):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        subject = "Have some query"
        message = name + "\n" + message + "\n" + email

        # print('>>>>>>>>>>>>>>>>',name,">>>>>>>>>>>>",message,'>>>>>>>>>>>',email)
        send_mail(subject=subject, message=message, from_email=email, recipient_list=[EMAIL_HOST_USER],
                  fail_silently=False)

        return redirect('contact')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    print("Activation------------------activate", account_activation_token.check_token(user, token))
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,"Your account is activated")
        return redirect('client-home')
    else:
        messages.success(request, "Your invitation link is invalid")
        return redirect('client-home')
