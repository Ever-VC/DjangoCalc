import matplotlib
matplotlib.use('Agg')  # Usar el backend 'Agg' para evitar problemas con el hilo principal

import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from .punto_fijo import *
from .validate_func import validate_func
import base64
import numpy as np
import sympy as sp
from sympy.core import Mul, Pow
import pandas as pd
import re # Regular expressions
from .extrapolacion_richardson import solve_extrapolacion_richardson, graficar_extrapolacion_richardson
from .models import Calculator_History


# Create your views here.
def index(request):
    if request.method == 'POST':
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

def history(request):
    # Obtiene el historial de cálculos del usuario autenticado y lo ordena por fecha de creación
    history = Calculator_History.objects.filter(user=request.user).order_by('-created_at') # Obtiene el historial de cálculos del usuario autenticado
    # Si no hay historial, retorna el template sin datos
    if not history:
        return render(request, 'history.html')

    # Recorre el historial y modifica el campo created_at para mostrar 'Hace cuánto tiempo se creó'
    # Formatea la fecha y hora para cada objeto
    for item in history:
        if item.verify_convergence == True:
            item.verify_convergence = 'checked'
    return render(request, 'history.html', {'history': history})

def exercise_delete(request, exercise_id):
    # Obtiene el ejercicio a eliminar
    exercise = Calculator_History.objects.get(id=exercise_id)
    exercise.delete() # Elimina el ejercicio
    return redirect('history') # Redirige al historial de cálculos

def punto_fijo(request):
    if request.method == 'POST':
        # Almacena los datos del formulario
        fx = request.POST['fx']
        gx = request.POST['gx']
        x0 = request.POST['x0']
        error_objetivo = request.POST['error']
        max_iter = request.POST['max_iter']
        decimals = request.POST['decimals']
        verify_convergence = request.POST.get('verify_convergence', False) # Verifica si verify_convergence está marcado

        if verify_convergence == 'on': # Si está marcado, entonces es True
            verify_convergence = True

        # Valida que los campos no estén vacíos
        if not fx or not x0 or not error_objetivo or not max_iter or not decimals:
            return render(request, 'punto_fijo.html', {
                'error': 'Todos los campos son obligatorios.'
            })
        
        # Elimina las , de los números decimales
        error_objetivo = error_objetivo.replace(',', '.')
        x0 = x0.replace(',', '.')

        # Valida que los campos numéricos sean válidos
        if not error_objetivo.replace('.', '', 1).isdigit() or not max_iter.isdigit() or not decimals.isdigit():
            return render(request, 'punto_fijo.html', {
                'error': 'Los campos error, iteraciones y decimales deben ser números.'
            })


        # Valida que la función f(x) y g(x) sean válidas
        try:
            if validate_func(fx) and validate_func(gx):
                fx = validate_func(fx)
                gx = validate_func(gx)
                gx_latex = sp.latex(gx)
            else:
                return render(request, 'punto_fijo.html', {
                    'error': 'La función f(x) o g(x) no es válida.'
                })
        except:
            return render(request, 'punto_fijo.html', {
                'error': 'La función f(x) o g(x) no es válida.'
            })

        # Calcula la derivada de la función g(x)
        x = sp.symbols('x') # Define la variable simbólica x
        gx_derivada = sp.diff(sp.sympify(gx), x) # Calcula la derivada de la función g(x)
        result_convergence = round(gx_derivada.evalf(subs={x: x0}), int(decimals)) # Evalúa la función derivada g'(x) en el punto x0
        gx_derivada_latex = sp.latex(gx_derivada)
        
        # Verifica la convergencia solo si verify_convergence está marcado
        #if verify_convergence and not validar_gx(gx, float(x0)):
        if verify_convergence and not (0 <= float(result_convergence) <= 1): # Verifica que el resultado esté en el intervalo [0, 1]
            # Retorna el template con el error de convergencia
            return render(request, 'punto_fijo.html', {
                'error': 'La función g(x) no converge en el punto x0 = ' + x0 + ", asegúrese de que g(x) sea continua y cumpla con la condición 0 <= g'(x) <= 1.",
                'convergence': None,
                'gx': gx_latex,
                'gx_derivada': gx_derivada_latex,
                'result_convergence': result_convergence,
                'x0': x0,
            })
        else: # Si la función g(x) converge, entonces calcula la raíz
            # Calcula la raíz de la función f(x) mediante el método del punto fijo
            df = solve_punto_fijo(gx, float(x0), float(error_objetivo), int(max_iter), int(decimals))
            # Grafica la función f(x) y el punto fijo
            image_png = graficar_punto_fijo(fx, df['X'].iloc[-1])

            # Convierte el DataFrame a una lista de diccionarios para mostrarlo en el template
            df = df.to_dict('records')

            for i in range(len(df) - 1):
                df[i]['Error'] = df[i + 1]['Error'] # El error es el siguiente valor de del error
                df[i]['Next_X'] = df[i + 1]['X']
            
            df[-1]['next_X'] = None # La última iteración no tiene siguiente valor

            # Guarda el historial de cálculos en la base de datos
            history = Calculator_History(
                method='punto_fijo',
                fx=fx,
                gx=gx,
                verify_convergence=verify_convergence,
                x0=x0,
                error=error_objetivo,
                max_iter=max_iter,
                decimals=decimals,
                user=request.user
            )

            history.save() # Guarda el historial de cálculos en la base de datos

            # Retorna el template con los resultados
            return render(request, 'punto_fijo.html', {
                'df': df,
                'image_png': image_png,
                'result': str(df[-1]['X']),
                'gx': gx_latex,
                'gx_derivada': gx_derivada_latex,
                'result_convergence': result_convergence,
                'convergence': validar_gx(gx, float(x0)),
                'x0': x0,
            })
    else: # Si el método es GET, retorna el template
        return render(request, 'punto_fijo.html')


def extrapolacion_richardson(request):
    if request.method == 'POST':
        fx = request.POST.get('fx')
        x0 = request.POST.get('x0')
        h = request.POST.get('h')
        order = int(request.POST.get('order'))

        # Valida que los campos no estén vacíos
        if not fx or not x0 or not h or not order:
            return render(request, 'extrapolacion_richardson.html', {
                'error': 'Todos los campos son obligatorios.'
            })
        
        # Elimina las , de los números decimales
        h = h.replace(',', '.')
        x0 = x0.replace(',', '.')
        
        h = float(h)
        x0 = float(x0)
        
        try:
            expr = validate_func(fx)
            
            f = sp.lambdify(sp.symbols('x'), expr, 'numpy')
            
            result, df_x_h_vals, df_extaplo_rich = solve_extrapolacion_richardson(f, x0, h, expr, order)
            graph = graficar_extrapolacion_richardson(f, x0, h, order, expr)

            df_x_h_vals = df_x_h_vals.to_dict('records')
            df_extaplo_rich = df_extaplo_rich.to_dict('records')
            
            graph_base64 = base64.b64encode(graph.getvalue()).decode('utf-8')

            # Guarda el historial de cálculos en la base de datos
            history = Calculator_History(
                method='extrapolacion_richardson',
                fx=fx,
                x0=x0,
                h=h,
                order=order,
                user=request.user
            )

            history.save() # Guarda el historial de cálculos en la base de datos

            context = {
                'result': result,
                'graph': graph_base64,
                'fx': sp.latex(expr),
                'df_x_h_vals': df_x_h_vals,
                'df_extaplo_rich': df_extaplo_rich,
                'order': order,
            }
            return render(request, 'extrapolacion_richardson.html', context)
        except ValueError as e:
            return render(request, 'extrapolacion_richardson.html', {'message': str(e)})
    else:
        return render(request, 'extrapolacion_richardson.html')
