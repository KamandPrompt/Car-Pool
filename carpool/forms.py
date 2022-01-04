from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from .models import User, Pool

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'password1', 'password2', )


CHOICE = (
    ("Mandi", _("Mandi")),
    ("South Campus", _("South Campus")),
    ("North Campus", _("North Campus")),
)


class PoolForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    tot = forms.IntegerField(widget=forms.NumberInput(), label="Seats")
    dateTime = forms.CharField(widget=forms.TextInput(attrs={'id':'datepicker-3'}))
    source = forms.ChoiceField(choices=CHOICE, initial='', widget=forms.Select())
    dest = forms.ChoiceField(choices=CHOICE, label="destination", initial='', widget=forms.Select())
    paid = forms.BooleanField(required=False)
    amount = forms.IntegerField(widget=forms.NumberInput(), required=False)

    class Meta:
        model = Pool
        fields = ('user', 'tot', 'dateTime', 'source', 'dest', 'paid', 'amount',)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PoolForm, self).__init__(*args, **kwargs)


CHOICES = (
    (1, _("Mandi")),
    (2, _("South Campus")),
    (3, _("North Campus")),
)


class filterForm(forms.Form):
    source = forms.ChoiceField(choices=CHOICES, label="From", initial='', widget=forms.Select())
    dest = forms.ChoiceField(choices=CHOICES, label="To", initial='', widget=forms.Select())
    free = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))
    tot = forms.IntegerField(widget=forms.NumberInput(), label="Slots")
    date = forms.CharField(widget=forms.TextInput(attrs={'id':'datepicker-3'}))


class DeleteForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput())


class AddForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput())
