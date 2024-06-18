from django.shortcuts import render

# Create your views here.
def punto_fijo(request):
    return render(request, 'punto_fijo.html', name='punto_fijo')