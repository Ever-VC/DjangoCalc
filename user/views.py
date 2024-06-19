from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        
        if password == confirm_password:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return render(request, 'index.html', {'message': 'Usuario creado con éxito.'})
            except:
                return render(request, 'signup.html', {'error': 'El usuario ya existe.'})
        else:
            return render(request, 'signup.html', {'error': 'Las contraseñas no coinciden.'})
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.check_password(password):
                login(request, user)
                return redirect('index')
            return render(request, 'registration.html', {'error': 'Contraseña incorrecta.'})
        return render(request, 'registration.html', {'error': 'El usuario no existe.'})