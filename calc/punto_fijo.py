# Importa los módulos necesarios
import matplotlib
matplotlib.use('Agg')  # Usar el backend 'Agg' para evitar problemas con el hilo principal

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import pandas as pd
import io
import base64


# Valida que la función g(x) sea válida (verifica la convergencia)
def validar_gx(gx, x0):
    x = sp.symbols('x') # Define la variable simbólica x
    g_derivada = sp.diff(sp.sympify(gx), x) # Calcula la derivada de la función g(x)
    result = g_derivada.evalf(subs={x: x0}) # Evalúa la función derivada g'(x) en el punto x0
    return 0 <= float(result) <= 1 # Verifica que el resultado esté en el intervalo [0, 1]

# Define la función que implementa el método del punto fijo para encontrar la raíz de una función
def solve_punto_fijo(gx, x_previo, error_objetivo, max_iter, decimals):
    # Inicializa las variables
    x = sp.symbols('x')
    iteraciones = 0

    # Crea un DataFrame para almacenar los resultados tales como: cada valor de x en la iteración, el error y la función evaluada en x y las iteraciones
    df = pd.DataFrame(columns=['Iteración', 'X', 'Error'])
    df.loc[len(df)] = [iteraciones, round(x_previo, decimals), error_objetivo]
    # Itera hasta que se alcance el error objetivo
    while (iteraciones + 1) <= max_iter:
        # Calcula el valor de x en la iteración actual
        xi = round(gx.evalf(subs={x: x_previo}), decimals)
        # Calcula el error absoluto
        error = round(abs((xi - x_previo) / xi) * 100, decimals)

        # Almacena los resultados en el DataFrame
        df.loc[len(df)] = [iteraciones, xi, error]
        # Verifica si se alcanzó el error objetivo
        if error < error_objetivo:
            break

        # Actualiza el valor de x_previo para la siguiente iteración
        x_previo = xi
        iteraciones += 1

    # Redondea los resultados a la cantidad de decimales especific
    df = df.round(decimals)

    return df # Retorna el DataFrame con los resultados


def graficar_punto_fijo(fx, raiz):
    x = sp.symbols('x')  # Define la variable simbólica x

    if 'sqrt' in str(fx):  # Verifica si la función contiene la raíz cuadrada
        number = np.linspace(0, 40, 100)  # Crea un arreglo de números para evaluar la función f(x)
    else:
        number = np.linspace(-10, 10, 100)

    plt.figure()  # Crea una nueva figura

    # Grafica la función f(x) en el intervalo [-10, 10] y añade etiqueta
    plt.plot(number, [fx.evalf(subs={x:i}) for i in number], label='f(x)')  

    # Marca la raíz en la gráfica de f(x) y añade etiqueta y color rojo
    plt.plot(raiz, [fx.evalf(subs={x:raiz})], marker='o', label='Raíz aproximada', color='red')  

    # Etiqueta la raíz en la gráfica de f(x) con el valor de la raíz y una flecha
    plt.annotate(str(raiz), (raiz, fx.evalf(subs={x:raiz})), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.grid()  # Activa la cuadrícula en la gráfica
    plt.xlim(-2, 20)  # Establece los límites del eje x en la gráfica
    plt.ylim(-10, 10)  # Establece los límites del eje y en la gráfica
    plt.axhline(0, color='black')  # Agrega una línea horizontal en y=0
    plt.axvline(0, color='black')  # Agrega una línea vertical en x=0
    plt.legend()  # Muestra la leyenda en la gráfica
    plt.title('Gráfica de f(x) y raíz aproximada')  # Establece el título de la gráfica

    buffer = io.BytesIO()  # Crea un buffer de bytes
    plt.savefig(buffer, format='png')  # Guarda la gráfica en el buffer en formato PNG
    buffer.seek(0)  # Mueve el cursor al inicio del buffer
    image_png = base64.b64encode(buffer.getvalue()).decode()  # Codifica el buffer en base64 y lo convierte a cadena de texto
    buffer.close()  # Cierra el buffer

    return image_png  # Retorna la imagen en formato base64

    
    

