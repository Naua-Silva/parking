# Parking

# API de controle de estacionamento com Django Rest Framework

# Ações disponíveis:
# Entrada:
# url: '/parking'
# Recebe a placa de um veículo, valida a máscara AAA-9999 e retorna um número de "reserva"

# Pagamento:
# url: '/{id}/pay' ou '/pay'
# Recebe o número de "reserva" e a marca como "paga"

# Saída:
# url: '/{id}/out' ou '/out'
# Recebe o número de "reserva" e libera a saída caso a "reserva" esteja marcada como "paga"

# Histórico:
# url: '/parking/{plate}'
# Recebe uma placa e retorna um histórico de reservas relacionadas com a placa, fornecendo 'número da reserva' e 'tempo estacionado'
