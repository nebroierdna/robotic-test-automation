import serial
import time

# Setup
# Configurações da porta serial
port = 'COM9'  # Substitua pela porta correta
baudrate = 115200  # Taxa de baud padrão para GRBL

# Inicializa a conexão serial
ser = serial.Serial(port, baudrate)
time.sleep(2)  # Aguarda a inicialização da conexão


def send_gcode(command):
    ser.write(f'{command}\n'.encode())
    response = ser.readline().decode().strip()
    print("Resposta da máquina:", response)
    return response

def perform_touch(x, y, z):
    send_gcode(f"X{x} F2000")
    send_gcode(f"Y{y} F2000")  
    send_gcode(f"Z{z} F2000")


#PRECONDITION
# Set zero
send_gcode("G10 P0 L20 X0 Y0 Z0")

# Define as unidades de medida para mm e pos. relativa a posição anterior
send_gcode("G21 G91")
time.sleep(2)

#ACTION
perform_touch(0, 0, 4)
time.sleep(0.5)
perform_touch(0, 0, 4)
time.sleep(5)

#POSTCONDITION
# Mover de volta pro zero
send_gcode("G90 G1 X0 Y0 F1000")

# Fecha a conexão serial
ser.close()

# ================================================================================
# UGS commands and knowledge
# X, Y, Z: Eixo no qual quero movimentar + número do step size em mm - G0 X8 Y8 Z8
# F: Feed rate em mm/min - G01 X10 Y10 Z10 F1500
# G0: movimentos rápidos - G0 X10 Y20 Z30
# G01: movimentos controlados - G01 X10 Y10 Z10 F1500
# G21: Define as unidades de medida para mm
# G90: Posicionamento absoluto (coord. relativas ao ponto 0)
# G91: Posicionamento relativo (coord. relativas ao ponto atual)
# G92: Redefine posição atual como novo zero - G92 X0 Y0 Z0

# Examplos do UGS
# Reset Zero: >>> G10 P0 L20 X0 Y0 Z0
# >>> $J = G21 G91 X8 F2000
# >>> $J = G21 G91 Y8 F2000
# >>> $J = G21 G91 Z8 F2000
# >>> $J = G21 G91 X-8 F2000
# >>> $J = G21 G91 Y-8 F2000
# >>> $J = G21 G91 Z-8 F2000
# >>> G90 G0 X0 Y0
# >>> G90 G0 Z0 (NO MEU CASO ESSE ÚLTIMO Z0 NÃO É PRA ACONTECER)

# Parâmetros
    # Definir limites máximos de deslocamento
    # x_max = 200.0  # Limite máximo para o eixo X em mm
    # y_max = 200.0  # Limite máximo para o eixo Y em mm
    # z_max = 200.0  # Limite máximo para o eixo Z em mm

    # send_gcode_command(f'$130={x_max}')
    # send_gcode_command(f'$131={y_max}')
    # send_gcode_command(f'$132={z_max}')


# 100, $101 and $102 – [X,Y,Z] steps/mm
# Grbl needs to know how far each step will take the tool in reality. To calculate steps/mm for an axis of your machine you need to know:

# The mm traveled per revolution of your stepper motor. This is dependent on your belt drive gears or lead screw pitch.
# The full steps per revolution of your steppers (typically 200)
# The microsteps per step of your controller (typically 1, 2, 4, 8, or 16). Tip: Using high microstep values (e.g., 16) can reduce your stepper motor torque, so use the lowest that gives you the desired axis resolution and comfortable running properties.
# The steps/mm can then be calculated like this: steps_per_mm = (steps_per_revolution*microsteps)/mm_per_rev

# Compute this value for every axis and write these settings to Grbl.

# $130, $131, $132 - [X,Y,Z] Max travel, mm
# This sets the maximum travel from end to end for each axis in mm. 
# This is only useful if you have soft limits (and homing) enabled, 
# as this is only used by Grbl's soft limit feature to check if you have exceeded your machine limits with a motion command.