import serial
import time

# Configurações da porta serial
port_grbl = 'COM4'  # Substitua pela porta correta para GRBL
port_arduino = 'COM9'  # Porta para o Arduino ligado à tela touch
baudrate_grbl = 115200  # Taxa de baud padrão para GRBL
baudrate_arduino = 9600  # Taxa de baud padrão para Arduino

# Inicializa a conexão serial
ser_grbl = serial.Serial(port_grbl, baudrate_grbl)
ser_arduino = serial.Serial(port_arduino, baudrate_arduino)
time.sleep(2)  # Aguarda a inicialização da conexão

# Variáveis para cálculo de precisão
total_touches = 0
registered_touches = 0

def send_gcode(command):
    ser_grbl.write(f'{command}\n'.encode())
    response = ser_grbl.readline().decode().strip()
    print("Resposta da máquina:", response)
    return response

def perform_touch(x, y, z):
    send_gcode(f"G1 X{x} F2000")
    send_gcode(f"G1 Y{y} F2000")  
    send_gcode(f"G1 Z{z} F1500")

# Função para ler as coordenadas do toque do Arduino
def read_touch_coordinates(discard_first=False):
    global registered_touches
    if ser_arduino.in_waiting:
        line = ser_arduino.readline().decode('utf-8').strip()
        if "X = " in line and "\tY = " in line:
            try:
                x_str = line.split("X = ")[1].split("\t")[0]
                y_str = line.split("\tY = ")[1]
                x, y = int(x_str), int(y_str)
                print(f"Coordenadas do toque: X = {x}, Y = {y}")

                if not discard_first:
                    registered_touches += 1

                return x, y
            except ValueError:
                print(f"Valor inválido recebido: {line}")
    return None

# Função para mostrar a precisão dos toques
def show_accuracy():
    accuracy = (registered_touches / total_touches) * 100 if total_touches > 0 else 0
    print(f"Precisão de toque: {accuracy:.2f}%")

# PRECONDITION
# Set zero
send_gcode("G10 P0 L20 X0 Y0 Z0")

# Define as unidades de medida para mm e pos. relativa a posição anterior
send_gcode("G21 G91")
time.sleep(2)

# Desconsiderar a primeira leitura para descartar qualquer ruído
print("Descartando primeira leitura...")
read_touch_coordinates(discard_first=True)

# ACTION
number_of_touch_executions = 1
perform_touch(-11, -56, 0)
time.sleep(3)
for touch in range(number_of_touch_executions):
    perform_touch(0, 0, 8)
    total_touches += 1
    time.sleep(3)
    coordinates = read_touch_coordinates()
    if coordinates:
        x, y = coordinates
        print(f"Toque registrado nas coordenadas: X = {x}, Y = {y}")
    else:
        print("Nenhum toque registrado.")

# POSTCONDITION
# Mover de volta pro zero
send_gcode("G90 G1 X0 Y0 F1000")

# Exibir a precisão dos toques
show_accuracy()

# Fecha a conexão serial
ser_grbl.close()
ser_arduino.close()
