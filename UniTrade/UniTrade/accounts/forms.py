                    ###   AUTHOR: ZIYAD ELGYZIRI   ###



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Import your custom user model

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # Use your custom user model
        fields = ['email', 'password1', 'password2']  # Adjust fields as needed
