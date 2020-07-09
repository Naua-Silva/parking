from django.shortcuts import render
from django.contrib import messages
from .models import *

def index(request):

	return render(request, 'parking/index.html')

def goingIn(request):

	if request.method == 'POST':
		placa = request.POST.get('plate')

		if placa is not "":
			teste1 = Reserve.objects.filter(plate=placa, In=True)
			if teste1:
				teste2 = Reserve.objects.filter(plate=placa, In=True, paid=False)
				teste3 = Reserve.objects.filter(plate=placa, In=True, paid=True)
				if teste2:
					teste = Reserve.objects.get(plate=placa, In=True, paid=False)
					messages.error(request, 'Veículo já dentro, para sair pague a reserva {}'.format(teste.id))
				elif teste3:
					messages.error(request, 'Veículo já dentro com saída liberada')
			else:
				reserva = Reserve.objects.create(plate=placa)
				messages.error(request, 'Número da reserva: {}'.format(reserva.id))

		else:
			messages.error(request, 'Digite uma placa válida')


	return render(request, 'parking/entrada.html')