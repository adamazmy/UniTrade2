                    ###   AUTHOR: ZIYAD ELGYZIRI   ###


from django.urls import path
from . import views  # Import views from current app
from django.contrib.auth import views as auth_views  # Import Django's login view


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    
]