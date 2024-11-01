import serial
import time

port = '/dev/ttyUSB0'
baud_rate = 115200

ser = serial.Serial(port, baud_rate, timeout=1)
time.sleep(2)

def send_command(command):
    ser.flushInput()
    ser.write(f"{command}\n".encode())
    time.sleep(1)
    while ser.in_waiting:
        response = ser.readline().decode('utf-8').strip()
        if response:
            print(f"response: {response}")

def check_grbl_state():
    send_command('$$') # request configurações atuais
    send_command('?') # request estado atual do grbl

check_grbl_state()
send_command('$X') # Desbloqueia o grbl
time.sleep(1)
check_grbl_state()

send_command('G1 X10 F100')

ser.close()