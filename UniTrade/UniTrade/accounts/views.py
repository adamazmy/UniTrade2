                    ###   AUTHOR: ZIYAD ELGYZIRI   ###



from django.shortcuts import render, redirect
from .models import CustomUser  # Replace with your custom form if applicable
from .forms import SignupForm  # Import your custom signup form (optional)
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token



def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)  # Use custom form if applicable
    if form.is_valid():
        user = form.save()
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Email Verification - UniTrade"
        message2 = render_to_string('email_confirmation.html',{
            
            'email': user.email,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [user.email],
        )
        email.fail_silently = True
        email.send()

        return render(request, 'registration/signup_success.html',{})
  else:
    form = SignupForm()  # Use custom form if applicable
  return render(request, 'registration/signup.html', {'form': form})


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = CustomUser.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,CustomUser.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        return redirect('signup')

