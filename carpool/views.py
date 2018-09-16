from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm as LoginForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token

from .forms import SignUpForm, PoolForm


def IITmail(request):
    s = request.POST['email']
    str = s[-14:]
    if str.lower() == "iitmandi.ac.in":
        return True
    else:
        return False


def new(request):
    error=""
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not IITmail(request):
            error+="Please use an IIT Mandi email."
        elif not form.is_valid():
            error+="Invalid information/ Email already in use."
        else:
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': user.pk,
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'error': error, })


def dashboard(request):
    return


def addPool(request):
    return
