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

# Desbloqueia o grbl
send_command('$X')
time.sleep(1)

send_command('$I')
time.sleep(2)

send_command('G0 X10')
time.sleep(2)

ser.close()