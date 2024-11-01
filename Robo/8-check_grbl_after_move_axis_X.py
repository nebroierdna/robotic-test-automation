import serial
import time

# Configuração da porta serial
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Substitua '/dev/ttyUSB0' pela porta correta
time.sleep(2)  # Aguarde a inicialização da conexão

# Enviar comando de desbloqueio
ser.write(b'$X\n')  # Desbloqueia o GRBL
time.sleep(1)  # Aguarde um momento para a resposta

# Ler todas as respostas disponíveis
while ser.in_waiting > 0:
    response = ser.readline().decode('utf-8').strip()
    print("Resposta do Arduino:", response)

# Enviar comando para mover o motor X
ser.write(b'G1 X10 F100\n')  # Move o motor X para a posição 10 com uma velocidade de 100 mm/min
time.sleep(1)  # Aguarde um momento para a resposta

# Enviar comando de status para verificar o estado
ser.write(b'?\n')  # Envia comando de status
time.sleep(1)  # Aguarde um momento para a resposta

# Ler todas as respostas disponíveis
while ser.in_waiting > 0:
    response = ser.readline().decode('utf-8').strip()
    print("Status do GRBL:", response)

ser.close()
