import serial
import time
import sys

# Setup
# Configurações da porta serial
port = 'COM9'  # Substitua pela porta correta
baudrate = 115200  # Taxa de baud padrão para GRBL

# Inicializa a conexão serial
ser = serial.Serial(port, baudrate)
time.sleep(2)  # Aguarda a inicialização da conexão

# ==================================================================================
# Library
# ==================================================================================
# Functions
def send_gcode(command):
    ser.write(f'{command}\n'.encode())
    response = ser.readline().decode().strip()
    print("Resposta da máquina:", response)
    return response

def perform_touch(x,y):
    send_gcode(f"X{x} F2000")
    send_gcode(f"Y{y} F2000")  
    send_gcode("Z8 F2000")

def find_icon():
	pass

def find_text():
	pass

def get_coordinates():
	pass	

def find_icon_and_touch(icon):
    try:
        icon_found, coordinates = find_icon(icon)
        if icon_found:
            x,y = get_coordinates(coordinates)
            perform_touch(x,y)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def find_text_and_touch(search_string):
    try:
        string_found, coordinates = find_text(search_string)
        if string_found:
            x,y = get_coordinates(coordinates)
            perform_touch(x,y)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def open_app(app):
    try: 
        find_icon_and_touch(app)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def check_submenus(app, submenu):
    submenu_found = False
    try: 
        # Enter app submenu
        find_text_and_touch(app)

        # Check header
        submenu_found = find_text(submenu)
        return submenu_found
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# ==================================================================================
# Testcases
# ==================================================================================
# Check submenus
# ==================================================================================
# Precondition
# Go home
icon_path = '' # Inserir aqui caminho pro png do ícone
find_icon_and_touch(icon_path)

# ==================================================================================
# Action
# Open app
open_app()

# Check app submenus
submenu_found = check_submenus()

# Testcase validation and verdict
if submenu_found:
     print('Test Passed')
else:
     print('Test Failed')

# ==================================================================================
# Postcondition
# Go home
icon_path = '' # Inserir aqui caminho pro png do ícone
find_icon_and_touch(icon_path)
# ==================================================================================