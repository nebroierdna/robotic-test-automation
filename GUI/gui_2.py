import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtGui import QFont

class AutomotivoApp(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Sistema Automotivo")
        self.setGeometry(300, 300, 400, 200)

        # Fundo preto para o HOME
        self.setStyleSheet("background-color: black;")

        # Rótulo para exibir a hora
        self.time_label = QLabel(self)
        self.time_label.move(300, 10)
        self.time_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.time_label.setStyleSheet("color: white;")

        # Botão para ir para o APPS menu
        self.btn_apps = QPushButton('Ir para APPS', self)
        self.btn_apps.setGeometry(150, 150, 100, 30)
        self.btn_apps.clicked.connect(self.show_apps_menu)
        self.btn_apps.setStyleSheet("background-color: blue; color: white;")

        # Timer para atualizar a hora
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)  # Atualiza a cada segundo

        self.showTime()

    def showTime(self):
        current_time = QDateTime.currentDateTime()
        formatted_time = current_time.toString('hh:mm:ss')
        self.time_label.setText(formatted_time)

    def show_apps_menu(self):
        # Muda o fundo para azul escuro
        self.setStyleSheet("background-color: #00008B;")

        # Esconde o botão
        self.btn_apps.hide()

        # Adiciona novos elementos para o menu APPS (exemplo)
        # ...

        # Criando um layout para os widgets do menu APPS
        layout = QVBoxLayout()

        # Botão para monitorar sensores
        btn_sensores = QPushButton('Monitorar Sensores')
        btn_sensores.clicked.connect(self.monitorar_sensores)
        layout.addWidget(btn_sensores)

        # Botão para controlar dispositivos
        btn_dispositivos = QPushButton('Controlar Dispositivos')
        btn_dispositivos.clicked.connect(self.controlar_dispositivos)
        layout.addWidget(btn_dispositivos)

        # ... (outros botões para as demais funcionalidades)

        # Adicionando o layout à janela principal
        self.setLayout(layout)

    # Funções para cada botão (exemplos):
    def monitorar_sensores(self):
        # Código para ler dados dos sensores e exibir em uma interface gráfica
        pass

    def controlar_dispositivos(self):
        # Código para enviar comandos para os dispositivos
        pass

# Executa a aplicação
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutomotivoApp()
    window.show()
    sys.exit(app.exec_())