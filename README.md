# Proyecto de Solución de Ejercicios con Métodos Numéricos

![2](https://github.com/Ever-VC/DjangoCalc/assets/102596002/a1bd3e1a-08f9-4ce9-b1fc-0df0b9880a34)

## Descripción del Proyecto

<table>
  <tr>
    <td><img src="https://github.com/Ever-VC/DjangoCalc/assets/102596002/2c456385-9f44-4e58-ad40-56fb5ee849e7" alt="Python-logo" width="100" height="100"></td>
    <td><img src="https://github.com/Ever-VC/DjangoCalc/assets/102596002/08f6dd01-026d-450b-89af-53dec2f0124e" alt="Django-logo" width="100" height="100"></td>
  </tr>
</table>

Este proyecto está desarrollado en Python y Django, y su objetivo es solucionar ejercicios utilizando dos métodos numéricos: el método de iteración de punto fijo y el método de extrapolación de Richardson.

## Contenidos

1. [Instalación](#instalación)
2. [Uso](#uso)
3. [Teoría de los Métodos](#teoría-de-los-métodos)
    - [Método de Iteración de Punto Fijo](#método-de-iteración-de-punto-fijo)
    - [Método de Extrapolación de Richardson](#método-de-extrapolación-de-richardson)
4. [Desarrolladores](#desarrolladores)
5. [Licencia](#licencia)

## Instalación

Para instalar y configurar el proyecto, sigue estos pasos:

1. Clona este repositorio:
    ```sh
    git clone https://github.com/tu_usuario/tu_repositorio.git
    ```
2. Navega al directorio del proyecto:
    ```sh
    cd tu_repositorio
    ```
3. Crea y activa un entorno virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```
4. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```
5. Realiza las migraciones:
    ```sh
    python manage.py migrate
    ```
6. Inicia el servidor de desarrollo:
    ```sh
    python manage.py runserver
    ```

## Uso

Para utilizar el proyecto, abre tu navegador y navega a `http://localhost:8000`. Sigue las instrucciones en la interfaz para solucionar ejercicios con los métodos disponibles.

## Teoría de los Métodos

### Método de Iteración de Punto Fijo

El método de iteración de punto fijo es una técnica para encontrar soluciones de ecuaciones de la forma \( x = g(x) \). La idea es empezar con una aproximación inicial \( x_0 \) y generar una secuencia mediante la iteración:
\[ x_{n+1} = g(x_n) \]
hasta que la secuencia converja a un punto fijo \( x^* \), que será la solución de la ecuación.

### Método de Extrapolación de Richardson

La extrapolación de Richardson es una técnica utilizada para acelerar la convergencia de una secuencia o para mejorar la precisión de una aproximación. Si tenemos una aproximación \( A(h) \) que depende de un parámetro \( h \), podemos obtener una mejor aproximación combinando valores de \( A \) con diferentes \( h \) mediante las fórmulas:
![image](https://github.com/Ever-VC/DjangoCalc/assets/102596002/bca5aba7-6d06-400e-81d0-f8e6f2bec74d)

En este proyecto, utilizamos \( O(h^4) \) para calcular derivadas aproximadas. Esto nos permite obtener una precisión mejorada en las aproximaciones de las derivadas al utilizar el método de Richardson.

## Desarrolladores

- **Desarrollador 1**: Beatriz Jiménez
  - **Carnet**: CJ21004
  - **Responsabilidad**: Implementación del método de iteración de punto fijo y documentación.

- **Desarrollador 2**: Ever Vásquez
  - **Carnet**: VC21033
  - **Responsabilidad**: Implementación del método de extrapolación de Richardson y pruebas unitarias.

- **Desarrollador 3**: Mélida Fuentes
  - **Carnet**: 
  - **Responsabilidad**: Error 404 - Page Not Found.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
