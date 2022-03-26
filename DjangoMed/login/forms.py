from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


#form to user logging in
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
