import serial
import time

# Configurações da porta serial
port = 'COM9'  # Substitua pela porta correta
baudrate = 115200  # Taxa de baud padrão para GRBL

# Inicializa a conexão serial
ser = serial.Serial(port, baudrate)
time.sleep(2)  # Aguarda a inicialização da conexão

# Envia um comando G-code para mover o eixo X
# gcode_command = "G01 Y40 F1500\n"  # Move o eixo X para 10 mm a uma taxa de 1000 mm/min
gcode_command = "G21 G91 Z8 F2000\n"  
ser.write(gcode_command.encode())

# Aguarda a resposta da máquina
response = ser.readline().decode()
print("Resposta da máquina:", response)

# Fecha a conexão serial
ser.close()

#19/08/2024 - Observação: funcionou!