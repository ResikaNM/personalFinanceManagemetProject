from django import forms
from .models import Expens

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expens
        fields = ['name', 'date', 'category', 'description', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'category': forms.Select(choices=[('Health', 'Health'), ('Electronics', 'Electronics'),
                                              ('Travel', 'Travel'), ('Education', 'Education'),
                                              ('Books', 'Books'), ('Others', 'Others')]),
                  }

# class LoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
from django.contrib.auth.forms import AuthenticationForm
class LoginForm(AuthenticationForm):
    # You can customize this form further if needed
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
