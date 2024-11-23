import sys
import serial
from PyQt5.QtCore import QTimer, Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication

class MyApp:
    def __init__(self):
        self.arduino = serial.Serial('COM9', 9600, timeout=1)  # Ajuste 'COM9' para a porta serial correta
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(100)
        self.total_touches = 0
        self.valid_touches = 0
        self.first_value_read = True  # Flag para desconsiderar o primeiro valor lido

    def read_serial(self):
        if self.arduino.in_waiting:
            line = self.arduino.readline().decode('utf-8').strip()
            if "X = " in line and "\tY = " in line:
                try:
                    # Extrair e converter as coordenadas
                    x_str = line.split("X = ")[1].split("\t")[0]
                    y_str = line.split("\tY = ")[1]
                    x, y = int(x_str), int(y_str)
                    print(f"Coordenadas recebidas: X = {x}, Y = {y}")
                    if not self.first_value_read:
                        self.check_touch(x, y)
                    else:
                        self.first_value_read = False  # Desconsidera o primeiro valor lido
                except ValueError:
                    print(f"Valor inválido recebido: {line}")

    def check_touch(self, x, y):
        # Coeficientes da transformação linear
        a = 4.12105624
        b = -0.594478738
        c = -960.709877
        d = 1.5648834
        e = 0.389163237
        f = -544.320988

        # Calcular as coordenadas mapeadas usando a transformação linear
        mapped_x = int(a * x + b * y + c)
        mapped_y = int(d * x + e * y + f)

        print(f"Coordenadas mapeadas: X = {mapped_x}, Y = {mapped_y}")

        # Verificação se o ponto mapeado está dentro da faixa válida
        if 145 <= mapped_x <= 160 and 185 <= mapped_y <= 190:
            print("Toque válido detectado.")
            self.valid_touches += 1
        else:
            print("Erro de toque detectado.")
        self.total_touches += 1

    def show_accuracy(self):
        accuracy = (self.valid_touches / self.total_touches) * 100 if self.total_touches > 0 else 0
        print(f"Precisão de toque: {accuracy:.2f}%")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()

    # Definir um tempo de execução após o qual o programa será encerrado
    def quit_app():
        ex.show_accuracy()
        QCoreApplication.quit()

    QTimer.singleShot(30000, quit_app)  # Executa por 10 segundos e depois para
    sys.exit(app.exec_())
