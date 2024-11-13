import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from datetime import datetime

class CarSystem(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Sistema Multimídia")
        self.setGeometry(100, 100, 800, 480)  # Ajustar o tamanho conforme necessário

        # Layout principal
        layout = QVBoxLayout()

        # Barra superior com a hora
        self.time_label = QLabel(self)
        self.time_label.setStyleSheet("background-color: black; color: white; font-size: 20px;")
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.update_time()

        # Botão HOME
        home_button = QPushButton("HOME")
        home_button.setStyleSheet("background-color: black; color: white; border-radius: 10px;")
        home_button.clicked.connect(self.show_apps)

        # Adicionando elementos ao layout
        layout.addWidget(self.time_label)
        layout.addWidget(home_button)

        self.setLayout(layout)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(current_time)
        self.time_label.adjustSize()
        self.time_label.repaint()
        # Atualiza a hora a cada segundo
        self.timer = self.startTimer(1000)

    def show_apps(self):
        # Cria uma nova janela para os aplicativos
        self.apps_window = AppsWindow()
        self.apps_window.show()

class AppsWindow(QWidget):
    def __init__(self):
        super().__init__()
        # ... (implementação da janela de aplicativos)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    car_system = CarSystem()
    car_system.show()
    sys.exit(app.exec_())