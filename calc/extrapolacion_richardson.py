import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import pandas as pd
import io

def high_order_central_difference(f, x_val, h_val, order, df, expr):
    expr = str(expr)
    x, h = sp.symbols('x h')  # Definir las variables simbólicas
    f_sym = sp.Function('f')(x)  # Definir la función simbólica f(x)
    if order == 1:
        result = (-f(x_val + 2 * h_val) + 8 * f(x_val + h_val) - 8 * f(x_val - h_val) + f(x_val - 2 * h_val)) / (12 * h_val)
        fxip2 = sp.sympify(expr.replace('x', str(x_val + 2 * h_val)))
        fxip1 = sp.sympify(expr.replace('x', str(x_val + h_val)))
        fxim1 = sp.sympify(expr.replace('x', str(x_val - h_val)))
        fxim2 = sp.sympify(expr.replace('x', str(x_val - 2 * h_val)))
        df.loc[len(df)] = [x_val, h_val, result, sp.latex(fxip2), sp.latex(fxip1), sp.latex(fxim1), sp.latex(fxim2)]
    elif order == 2:
        result = (-f(x_val + 2 * h_val) + 16 * f(x_val + h_val) - 30 * f(x_val) + 16 * f(x_val - h_val) - f(x_val - 2 * h_val)) / (12 * h_val ** 2)
        fxip2 = sp.sympify(expr.replace('x', str(x_val + 2 * h_val)))
        fxip1 = sp.sympify(expr.replace('x', str(x_val + h_val)))
        fxim1 = sp.sympify(expr.replace('x', str(x_val - h_val)))
        fxim2 = sp.sympify(expr.replace('x', str(x_val - 2 * h_val)))
        df.loc[len(df)] = [x_val, h_val, result, sp.latex(fxip2), sp.latex(fxip1), sp.latex(fxim1), sp.latex(fxim2)]
    elif order == 3:
        result = (-f(x_val + 3 * h_val) + 8 * f(x_val + 2 * h_val) - 13 * f(x_val + h_val) + 13 * f(x_val - h_val) - 8 * f(x_val - 2 * h_val) + f(x_val - 3 * h_val)) / (8 * h_val ** 3)
        fxip2 = sp.sympify(expr.replace('x', str(x_val + 2 * h_val)))
        fxip1 = sp.sympify(expr.replace('x', str(x_val + h_val)))
        fxim1 = sp.sympify(expr.replace('x', str(x_val - h_val)))
        fxim2 = sp.sympify(expr.replace('x', str(x_val - 2 * h_val)))
        df.loc[len(df)] = [x_val, h_val, result, sp.latex(fxip2), sp.latex(fxip1), sp.latex(fxim1), sp.latex(fxim2)]
    elif order == 4:
        result = (f(x_val + 2 * h_val) - 4 * f(x_val + h_val) + 6 * f(x_val) - 4 * f(x_val - h_val) + f(x_val - 2 * h_val)) / (h_val ** 4)
        df.loc[len(df)] = [x_val, h_val, result]
    else:
        raise ValueError("Este programa soporta derivadas de hasta cuarto orden.")
    
    return result, df

def solve_extrapolacion_richardson(f, x, h, expr, order=1):
    df_x_h_vals = pd.DataFrame(columns=['Xval', 'Hval', 'dr',  'fxip2', 'fxip1', 'fxim1', 'fxim2'])

    D1, df_x_h_vals2 = high_order_central_difference(f, x, h, order, df_x_h_vals, expr)
    
    D2, df_x_h_vals3 = high_order_central_difference(f, x, h / 2, order, df_x_h_vals2, expr)

    error = round(abs((D2 - D1) / D1) * 100, 4)
    
    df_extapol_richard = pd.DataFrame(columns=['D1', 'D2', 'D', 'error'])
    
    D = (4/3) * D2 - (1/3) * D1
    df_extapol_richard.loc[len(df_extapol_richard)] = [D1, D2, D, error]
    
    return D, df_x_h_vals3, df_extapol_richard

def df_analitica(expr, order):
    x = sp.symbols('x')
    f_sym = sp.lambdify(x, expr, 'numpy')
    if order == 1:
        result = sp.diff(expr, x)
    elif order == 2:
        result = sp.diff(expr, x, 2)
    elif order == 3:
        result = sp.diff(expr, x, 3)
    elif order == 4:
        result = sp.diff(expr, x, 4)
    else:
        raise ValueError("Este programa soporta derivadas de hasta cuarto orden.")
    
    return result

def graficar_extrapolacion_richardson(f, x, h, order, expr):
    # Graficar la función f(x) y la derivada aproximada
    x_values = np.linspace(x - 2, x + 2, 400)
    f_values = [f(xi) for xi in x_values]
    
    df_approx = [high_order_central_difference(f, x0, h, order, pd.DataFrame(columns=['Xval', 'Hval', 'dr',  'fxp2', 'fxip1', 'fxim1', 'fxm2']), expr)[0] for x0 in x_values]

    # Calcular la derivada analítica y graficarla
    df_analitica_expr = df_analitica(expr, order)
    df_analitica_func = sp.lambdify(sp.symbols('x'), df_analitica_expr, 'numpy')
    df_analitica_values = [df_analitica_func(xi) for xi in x_values]

    fig, ax = plt.subplots()
    plt.axhline(0, color='black')  # Agrega una línea horizontal en y=0
    plt.axvline(0, color='black')  # Agrega una línea vertical en x=0
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)  # Agrega una grilla al gráfico

    ax.plot(x_values, f_values, label='f(x)')
    ax.plot(x_values, df_analitica_values, label='Derivada analítica') # Gráfico de la derivada analítica (línea punteada)
    ax.plot(x_values, df_approx, label='Derivada aproximada', linestyle=':') # Gráfico de la derivada aproximada usando Extrapolación de Richardson (línea punteada)

    ax.set_title(f'Derivada de orden {order}')

    # Añade una leyenda al gráfico
    ax.legend()
    
    ax.set_title(f'Derivada de orden {order}')
    ax.set_xlabel('x')
    ax.set_ylabel(f"f^{order}(x)")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    return buf
