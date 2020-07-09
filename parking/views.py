from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import *

@csrf_protect

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

def payment(request):
	if request.method == 'POST':
		id = request.POST.get('reserve')

		return redirect('{}/pay'.format(id))


	return render(request, 'parking/pagamento.html')

def paying(request, id):
	teste1 = Reserve.objects.filter(id=id)

	if teste1:
		teste2 = Reserve.objects.filter(id=id, In=True)
		if teste2:
			teste3 = Reserve.objects.filter(id=id, In=True, paid=True)
			teste4 = Reserve.objects.filter(id=id, In=True, paid=False)
			if teste3:
				messages.error(request, 'Esta reserva já foi paga')
			elif teste4:
				reserva = Reserve.objects.get(id=id)
				reserva.paid = True
				reserva.save()
				messages.error(request, 'Reserva paga com sucesso! Saída liberada para placa: {}'.format(reserva.plate))
	else:
		messages.error(request, 'Reserva inexistente')

	return redirect('pagamento')

def departure(request):

	if request.method == 'POST':
		id = request.POST.get('reserve')
		return redirect('{}/out'.format(id))

	return render(request, 'parking/saida.html')