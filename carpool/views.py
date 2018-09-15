from django.shortcuts import render


def IITmail(request):
    s = request.POST['email']
    str = s[-14:]
    if str.lower() == "iitmandi.ac.in":
        return True
    else:
        return False


def new(request):
    return


def dashboard(request):
    return


def addPool(request):
    return
