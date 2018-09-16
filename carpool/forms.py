from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Pool


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'password1', 'password2', )


class PoolForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    tot = forms.IntegerField(widget=forms.NumberInput())
    dateTime = forms.DateTimeField(widget=forms.widgets.DateTimeInput())
    source = forms.CharField(max_length=100)
    dest = forms.CharField(max_length=100)
    paid = forms.BooleanField()
    amount = forms.IntegerField(widget=forms.NumberInput())

    class Meta:
        model = Pool
        fields = ('user', 'tot', 'dateTime', 'source', 'dest', 'paid', 'amount',)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PoolForm, self).__init__(*args, **kwargs)
