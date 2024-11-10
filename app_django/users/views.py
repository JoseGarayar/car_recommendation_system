"""User views"""

# Django
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

# Forms
from app_django.users.forms import UserCreationForm

def unauthenticated_user(user):
    return not user.is_authenticated

@user_passes_test(unauthenticated_user, login_url='cars:home')
def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or reverse_lazy('cars:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Your email or password is incorrect!')
            return redirect(reverse_lazy('users:login'))
    else:
        return render(request, 'users/login.html', {'next': request.GET.get('next', '')})
    
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You were logout correctly!')
    return redirect(reverse_lazy('users:login'))

def signup_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form)
        print(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Cuenta creada exitosamente para {email}. ¡Ahora puedes iniciar sesión!')
            return redirect('users:login')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/signup.html', {'form': form})