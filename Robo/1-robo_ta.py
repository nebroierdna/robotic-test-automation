import serial
import time

# Configuração da porta serial
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Substitua '/dev/ttyUSB0' pela porta correta
time.sleep(2)  # Aguarde a inicialização da conexão

# Enviar comando
try:
    ser.write(b'G1 X10 F100\n')  # Envia comando G-code
except Exception as e:
    print(f"Error: {e}")    
ser.close()