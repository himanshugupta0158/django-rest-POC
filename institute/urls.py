from django.urls import path
from .views import HomePageView, LoginView, SignUpView, LogoutView

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', SignUpView.as_view(), name="signup"),
]