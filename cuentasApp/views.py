from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from cuentasApp.forms import RegistroForm


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, '¡Bienvenido/a, {}!'.format(usuario.username))
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'cuentasApp/registro.html', {'form': form})
