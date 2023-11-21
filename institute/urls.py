from django.urls import path
from .views import HomePageView, LoginView, SignUpView, LogoutView, LoggedInUserUpdate
# from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('user_update/', LoggedInUserUpdate.as_view(), name="user-update"),
    

    # Password reset django default NOTE : you need to setup email sending related settings in settings.py file 
    # path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', SignUpView.as_view(), name="signup"),
]