import serial
import time

# Configuração da porta serial
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Substitua '/dev/ttyUSB0' pela porta correta
time.sleep(2)  # Aguarde a inicialização da conexão

# Ler a mensagem de inicialização do GRBL
try:
    while ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print("Mensagem de inicialização do GRBL:", response)
except Exception as e:
    print(f"Error: {e}")    
ser.close()