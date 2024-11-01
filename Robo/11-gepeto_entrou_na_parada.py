import serial
import time

port = '/dev/ttyUSB0'
baud_rate = 115200

ser = serial.Serial(port, baud_rate, timeout=1)
time.sleep(2)

def send_command(command):
    ser.write(f"{command}\n".encode())
    time.sleep(1)
    while True:
        response = ser.readline().decode('utf-8').strip()
        if response:
            print(f"response: {response}")
            break

#command = '$I'
send_command('G0 X10')

ser.close()