from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def index(request):
    return render(request, 'index.html')

def documentacion(request):
    return render(request, 'documentacion.html')

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
                return redirect('index', {'message': 'Usuario creado con éxito.'})
            except:
                return render(request, 'signup.html', {'error': 'El usuario ya existe.'})
        else:
            return render(request, 'signup.html', {'error': 'Las contraseñas no coinciden.'})
    return render(request, 'signup.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('radio', False)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.check_password(password):
                login(request, user)
                if remember_me:
                    print('Remember me')
                    request.session.set_expiry(1209600) # Almacena la sesión por 2 semanas
                else:
                    print('Forget me')
                    request.session.set_expiry(0) # Almacena la sesión hasta que el navegador se cierre
                return redirect('index')
            return render(request, 'login.html', {'error': 'Contraseña incorrecta.'})
        return render(request, 'login.html', {'error': 'El usuario o la contraseña son incorrectos.'})
    return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Almacenar los datos del formulario
        username = request.POST.get('username')
        old_password = request.POST.get('password')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        user = request.user # Obtener el usuario actual
        if user.check_password(old_password): # Verificar la contraseña actual
            if password == confirm_password: # Verificar que las nuevas contraseñas coincidan
                user.username = username # Cambiar el nombre de usuario
                user.set_password(password) # Cambiar la contraseña
                user.save() # Guardar los cambios
                # Actualizar la sesión
                update_session_auth_hash(request, user)

                # Redirigir al perfil
                return redirect('profile')
            return render(request, 'edit_profile.html', {'error': 'Las contraseñas no coinciden.'})
        return render(request, 'edit_profile.html', {'error': 'Contraseña incorrecta.'})
    return render(request, 'edit_profile.html')