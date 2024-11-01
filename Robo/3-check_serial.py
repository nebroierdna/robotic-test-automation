import serial
import time

# Configuração da porta serial
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Substitua '/dev/ttyUSB0' pela porta correta
time.sleep(2)  # Aguarde a inicialização da conexão

# Enviar comando
try:
    ser.write(b'G1 X10 F100\n')  # Envia comando G-code
    time.sleep(1)  # Aguarde um momento para a resposta
    response = ser.readline().decode('utf-8').strip()
    print("Resposta do Arduino:", response)
except Exception as e:
    print(f"Error: {e}")    
ser.close()
