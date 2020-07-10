from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from .models import *

@csrf_protect

def index(request):

	return render(request, 'parking/index.html')

def goingIn(request):

	if request.method == 'POST':
		placa = request.POST.get('plate')
		if len(placa) == 8:
			if placa[3] == '-':
				if placa[:3].isalpha():		
					if placa[4:].isnumeric():
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
				else:
					messages.error(request, 'Digite uma placa válida')
			else:
				messages.error(request, 'Digite uma placa válida')
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

def goingOut(request, id):

	teste1 = Reserve.objects.filter(id=id)

	if teste1:
		teste2 = Reserve.objects.filter(id=id, In=True)
		if teste2:
			teste3 = Reserve.objects.filter(id=id, In=True, paid=False)
			if teste3:
				messages.error(request, 'Saída bloqueada, pague a reserva para poder sair')
			else:
				res = Reserve.objects.get(id=id)
				hora = datetime.now()
				hora2 = res.entryTime.replace(tzinfo=None)
				difTime = '03:00:00'
				formato = '%H:%M:%S'
				dif = (hora - hora2) + datetime.strptime(difTime, formato)

				res.departureTime = datetime.now()
				res.time = dif
				res.In = False

				res.save()
				
				messages.error(request, 'Até logo')
		else:
			messages.error(request, 'O veículo já saiu do estacionamento')

	else:
		messages.error(request, 'Reserva inexistente')

	return redirect('saida')

def searchHistory(request):
	if request.method == 'POST':
		placa = request.POST.get('plate')
		return redirect('parking/{}'.format(placa))

	return render(request, 'parking/pesquisar.html')

def searching(request, plate):
	if len(plate) == 8:
		if plate[3] == '-':
			if plate[:3].isalpha():		
				if plate[4:].isnumeric():
					reservas = Reserve.objects.filter(plate=plate)
					if reservas:
						context = {'reservas':reservas, 'plate':plate}
						return render(request, 'parking/pesquisado.html', context)
					else:
						messages.error(request, 'Nenhum histórico encontrado')
						return redirect('pesquisa')
				else: 
					messages.error(request, 'Digite uma placa válida')
					return redirect('pesquisa')
			else:
				messages.error(request, 'Digite uma placa válida')
				return redirect('pesquisa')
		else:
			messages.error(request, 'Digite uma placa válida')
			return redirect('pesquisa')
	else:
		messages.error(request, 'Digite uma placa válida')
		return redirect('pesquisa')