import sys
import time
import serial
import threading
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSignal, QObject

# Importe a classe MyApp do arquivo gui_6.py
from gui_6 import MyApp

# Configuração da porta serial (substitua 'COM4' pela porta correta no seu sistema)
ser = serial.Serial('COM4', 9600)
time.sleep(2)  # Aguarde a estabilização da conexão serial

class SerialReader(QObject):
    coordinates_received = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.running = True

    def read_from_arduino(self):
        while self.running:
            data = ser.readline().decode().strip()
            if data.startswith("X = ") and "\tY = " in data:
                parts = data.split("\tY = ")
                x_str = parts[0][4:]
                y_str = parts[1]
                self.coordinates_received.emit(int(x_str), int(y_str))
            time.sleep(0.1)

def map_coordinates(x, y):
    # Coordenadas conhecidas para mapear
    x_arduino, y_arduino = 511, 490
    x_gui, y_gui = 513, 308

    # Regra de 3 para ajustar as coordenadas proporcionalmente
    mapped_x = x * (x_gui / x_arduino)
    mapped_y = y * (y_gui / y_arduino)
    
    return int(mapped_x), int(mapped_y)

def test_button_click():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()

    button = window.getButton()
    
    # Imprime o texto do botão antes do clique
    print(f"Texto do botão antes do clique: {button.text()}")
    
    if button.text() != "MENU":
        print("Erro: O estado inicial do botão não é 'MENU'")
    
    # Contadores para a métrica
    correct_clicks = 0
    errors = 0

    def on_coordinates_received(x, y):
        nonlocal correct_clicks, errors
        print(f"Coordenadas recebidas: X = {x}, Y = {y}")
        # Emula o clique com as coordenadas recebidas ajustadas
        mapped_x, mapped_y = map_coordinates(x, y)
        print(f"Coordenadas mapeadas: X = {mapped_x}, Y = {mapped_y}")
        
        # Emula o clique na posição global usando pyautogui
        pyautogui.click(mapped_x, mapped_y)
        app.processEvents()
    
        # Imprime o texto do botão após cada clique
        print(f"Texto do botão: {button.text()}")
        
        # Verifica se o clique foi correto
        expected_text = "HOME" if button.text() == "MENU" else "MENU"
        if button.text() == expected_text:
            correct_clicks += 1
        else:
            errors += 1

        # Calcula a porcentagem de acerto dos toques
        total_clicks = correct_clicks + errors
        accuracy = (correct_clicks / total_clicks) * 100 if total_clicks > 0 else 0
        print(f"Porcentagem de acerto dos toques: {accuracy:.2f}%")
        print(f"Erros totais: {errors}")

    serial_reader = SerialReader()
    serial_reader.coordinates_received.connect(on_coordinates_received)

    thread = threading.Thread(target=serial_reader.read_from_arduino)
    thread.start()

    class MyAppWithMousePress(MyApp):
        def mousePressEvent(self, event):
            x = event.globalX()
            y = event.globalY()
            print(f"Coordenadas do clique manual: X = {x}, Y = {y}")
    
    MyAppWithMousePress()

    sys.exit(app.exec_())

if __name__ == '__main__':
    test_button_click()
