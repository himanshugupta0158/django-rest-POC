from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import BootstrapAuthenticationForm, BootstrapSignupForm


class HomePageView(View):
    
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        # form = SearchForm()
        print(request.user)
        # return render(request, self.template_name, {'form': form})
        return render(request, self.template_name)



class LoginView(View):
    def get(self, request):
        form = BootstrapAuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = BootstrapAuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  # Redirect to your home page

        return render(request, 'login.html', {'form': form})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    

class SignUpView(View):
    def get(self, request):
        form = BootstrapSignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = BootstrapSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to your home page

        return render(request, 'signup.html', {'form': form})