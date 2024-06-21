import sympy as sp
import re

def validate_func(func):
    # Define el símbolo x
    x = sp.symbols('x')

    # Realiza las sustituciones en la cadena de entrada
    func = func.replace('^', '**')

    # Realiza la sustitución de el número de Euler
    func = func.replace('e', str(sp.E))

    # Lista de caracteres permitidos (números, letras, operadores y paréntesis)
    allowed_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/^(). "

    # Validación de caracteres permitidos
    if not all(char in allowed_characters for char in func):
        raise ValueError("La entrada contiene caracteres no permitidos.")

    # Validación de variables permitidas (x)
    if not re.match(r'^[0-9a-zA-Z+\-*/^(). ]*$', func):
        raise ValueError("La entrada contiene caracteres no válidos.")

    # Verificar que los paréntesis estén balanceados
    if func.count('(') != func.count(')'):
        raise ValueError("Los paréntesis no están balanceados.")

    try:
        # Evalúa la cadena en una expresión de sympy y la retorna
        expr = sp.sympify(func)
    except Exception as e:
        raise ValueError(f"Error al procesar la expresión: {e}")

    return expr

