from django.shortcuts import render,redirect
from django.views import View
from django.core.mail import send_mail
from TuitionManagement.settings import EMAIL_HOST_USER


class ContactView(View):
    def get(self, request):
        return render(request, 'app/site/contact.html')

    def post(self, request):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        subject = "Have some query"
        message = name + "\n" + message+"\n"+email

        # print('>>>>>>>>>>>>>>>>',name,">>>>>>>>>>>>",message,'>>>>>>>>>>>',email)
        send_mail(subject=subject, message=message, from_email=email,recipient_list=[EMAIL_HOST_USER], fail_silently=False)

        return redirect('contact')
