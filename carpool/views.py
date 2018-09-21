from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm as LoginForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token

from .forms import SignUpForm, PoolForm, filterForm
from .models import Pool, User


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
            send_mail(mail_subject, message, 'b17110@students.iitmandi.ac.in', [to_email], fail_silently=False)
            # email = EmailMessage(mail_subject, message, to=[to_email])
            # email.send()
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'error': error, })


def log(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        error=""
        if request.method == 'POST':
            form = LoginForm(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error+="Invalid details."
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form, 'error': error})


def dashboard(request):
    if request.user.is_authenticated:
        allrides = Pool.objects.all()
        myrides = Pool.objects.filter(slots=request.user)
        if request.method == 'POST':
            filter = filterForm(request.POST)
            print(request.POST)
            indate = request.POST['date_year'] + '-' + request.POST['date_month'] + '-' + request.POST['date_day']
            CHOICES = {'1': "Mandi", '2': "South Campus", '3': "North Campus", }
            if 'free' in request.POST:
                allrides = Pool.objects.filter(source=CHOICES[request.POST['source']], dest=CHOICES[request.POST['dest']], tot__gte=request.POST['tot'], paid=False, dateTime__date = indate, )
            else:
                allrides = Pool.objects.filter(source=CHOICES[request.POST['source']], dest=CHOICES[request.POST['dest']], tot__gte=request.POST['tot'], paid=True, dateTime__date = indate, )
        else:
            filter = filterForm()
        return render(request, 'index.html', {'allrides': allrides, 'myrides': myrides, 'filter': filter, })
    else:
        return redirect('log')


def addPool(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PoolForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = PoolForm()
        return render(request, 'add.html', {'form': form})
    else:
        return redirect('log')


def activate(request, uidb64, token):
    try:
        user = User.objects.get(pk=uidb64)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    account_activation_token.check_token(user, token)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
