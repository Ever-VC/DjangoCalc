from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Profile

# Create your views here.
def index(request):
    return render(request, 'index.html')

def documentacion(request):
    return render(request, 'documentacion.html')

def calcular(request):
    return render(request, 'calcular.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        profile_img = request.FILES.get('profile_img')
        if password == confirm_password:
            try:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user.save()
                profile = Profile.objects.create(user=user, profile_img=profile_img)
                profile.save()
                login(request, user)
                return redirect('index')
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
    profile = Profile.objects.get(user=request.user)
    user = request.user
    return render(request, 'profile.html', {'user': user, 'profile_img': profile.profile_img})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Almacenar los datos del formulario
        user = request.user # Obtener el usuario actual
        first_name = request.POST.get('first_name', user.first_name)
        last_name = request.POST.get('last_name', user.last_name)
        username = request.POST.get('username', user.username)
        old_password = request.POST.get('password', user.password)
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        profile_img = request.FILES.get('profile_img', None)
        if user.check_password(old_password): # Verificar la contraseña actual
            if password == '': # Verificar si se ingresó una nueva contraseña
                password = old_password
                confirm_password = old_password

            if password == confirm_password: # Verificar que las nuevas contraseñas coincidan
                user.first_name = first_name
                user.last_name = last_name
                user.username = username # Cambiar el nombre de usuario
                user.set_password(password) # Cambiar la contraseña
                user.save() # Guardar los cambios
                
                # Actualizar la imagen de perfil si se subió una nueva
                if profile_img:
                    profile = Profile.objects.get(user=user)
                    profile.profile_img = profile_img
                    profile.save()

                # Actualizar la sesión
                update_session_auth_hash(request, user)

                # Redirigir al perfil
                return redirect('profile')
            return render(request, 'edit_profile.html', {'error': 'Las contraseñas no coinciden.'})
        return render(request, 'edit_profile.html', {'error': 'Contraseña incorrecta.'})
    profile = Profile.objects.get(user=request.user)
    return render(request, 'edit_profile.html', {'user': request.user, 'profile_img': profile.profile_img})