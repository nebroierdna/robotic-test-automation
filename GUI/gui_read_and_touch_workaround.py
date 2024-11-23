import sys
import serial
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt, QCoreApplication, QPoint, QMetaObject
from PyQt5.QtGui import QColor, QPalette, QFont, QMouseEvent

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.arduino = serial.Serial('COM9', 9600, timeout=1)  # Ajuste 'COM9' para a porta serial correta
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(100)
        self.total_touches = 0
        self.valid_touches = 0
        self.first_value_read = True  # Flag para desconsiderar o primeiro valor lido

    def initUI(self):
        self.setWindowTitle('PyQt GUI')
        self.showMaximized()

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        topBar = QHBoxLayout()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setStyleSheet("color: white; font-size: 40px; padding: 10px;")
        topBar.addWidget(self.label)

        topBarWidget = QWidget()
        topBarWidget.setLayout(topBar)
        topBarWidget.setFixedHeight(80)
        topBarWidget.setStyleSheet("background-color: black;")
        mainLayout.addWidget(topBarWidget)

        centerLayout = QVBoxLayout()
        centerLayout.addStretch()
        self.button = QPushButton('MENU', self)
        self.button.setFixedSize(150, 150)
        self.button.setFont(QFont('Arial', 18))
        self.button.setStyleSheet("""
            background-color: #5E9CD3; color: #003366;
            border-radius: 20px;
        """)
        self.button.clicked.connect(self.toggle)
        centerLayout.addWidget(self.button)
        centerLayout.addStretch()

        mainLayout.addLayout(centerLayout)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Window, QColor('#003366'))
        self.setPalette(p)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.showTime()

        # Ajustar a posição do botão para que a coordenada (160, 192) esteja dentro da área do botão
        self.fix_button_position()

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
                        self.emulate_click(x, y)
                    else:
                        self.first_value_read = False  # Desconsidera o primeiro valor lido
                except ValueError:
                    print(f"Valor inválido recebido: {line}")

    def toggle(self):
        if self.button.text() == 'MENU':
            self.button.setText('HOME')
            self.button.setFont(QFont('Arial', 18))
            self.button.setStyleSheet("""
                background-color: black; color: #5E9CD3;
                border-radius: 20px;
            """)
            p = self.palette()
            p.setColor(QPalette.Window, QColor('#5E9CD3'))
            self.setPalette(p)
        else:
            self.button.setText('MENU')
            self.button.setFont(QFont('Arial', 18))
            self.button.setStyleSheet("""
                background-color: #5E9CD3; color: #003366;
                border-radius: 20px;
            """)
            p = self.palette()
            p.setColor(QPalette.Window, QColor('#003366'))
            self.setPalette(p)
        self.fix_button_position()  # Fixar a posição após a mudança de estado
        print(f"Posição do botão após toggle: x = {self.button.pos().x()}, y = {self.button.pos().y()}")

    def showTime(self):
        currentTime = QTime.currentTime().toString('HH:mm:ss')
        self.label.setText(currentTime)

    def emulate_click(self, x, y):
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

        # Verificação se o ponto mapeado está dentro da área do botão
        button_rect = self.button.geometry()
        print(f'button_rect: {button_rect}')
        if button_rect.contains(mapped_x, mapped_y):
            print("Clique detectado dentro da área do botão.")
            self.valid_touches += 1
            QMetaObject.invokeMethod(self.button, "click", Qt.QueuedConnection)
        else:
            print("Clique fora da área do botão.")
        self.total_touches += 1
        self.show_accuracy()
        self.fix_button_position()  # Fixar a posição durante a emulação
        print(f"Posição do botão durante emulation: x = {self.button.pos().x()}, y = {self.button.pos().y()}")

    def show_accuracy(self):
        accuracy = (self.valid_touches / self.total_touches) * 100 if self.total_touches > 0 else 0
        print(f"Precisão de toque: {accuracy:.2f}%")

    def fix_button_position(self):
        self.button.move(160 - self.button.width() // 2, 192 - self.button.height() // 2)
        print(f"Nova posição do botão fixada: x = {self.button.pos().x()}, y = {self.button.pos().y()}")

    def get_coordinates(self):
        x = self.button.pos().x()
        y = self.button.pos().y()
        print(f"Coordenadas do botão: X = {x}, Y = {y}")
        return x, y

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            print(f"Coordenadas do clique manual: X = {x}, Y = {y}")
            self.get_coordinates()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
