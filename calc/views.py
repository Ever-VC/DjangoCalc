from django.shortcuts import render, redirect
import re # Regular expressions

# Create your views here.
def index(request):
    if request.method == 'POST':
        print(request.POST)
        basic_operation = request.POST.get('basic_operation')

        # Valida de que la operación solo contiene números y operadores básicos
        if re.match(r'^\d+(\s*[\+\-\*/]\s*\d+)*$', basic_operation):
            try:
                result = eval(basic_operation)
            except ZeroDivisionError:
                result = "Error: División por cero"
                return render(request, 'index.html', {'error': result})
            except Exception as e:
                result = f"Error: {e}"
                return render(request, 'index.html', {'error': result})
        else:
            result = "Error: Operación no válida"
            return render(request, 'index.html', {'error': result})

        return render(request, 'index.html', {'result': result})
    return render(request, 'index.html')

def basic_calc(request):
    if request.method == 'POST':
        print(request.POST)
        basic_operation = request.POST.get('basic_operation')

        # Valida de que la operación solo contiene números y operadores básicos
        if re.match(r'^\d+(\s*[\+\-\*/]\s*\d+)*$', basic_operation):
            try:
                result = eval(basic_operation)
            except ZeroDivisionError:
                result = "Error: División por cero"
                return render(request, '/', {'error': result})
            except Exception as e:
                result = f"Error: {e}"
                return render(request, '/', {'error': result})
        else:
            result = "Error: Operación no válida"
            return render(request, '/', {'error': result})

        return render(request, '/', {'result': result}) # Redirige a la página principal con el resultado
    else:
        return redirect('/')


def punto_fijo(request):
    return render(request, 'punto_fijo.html')
