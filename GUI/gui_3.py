import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QColor, QPalette

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('PyQt GUI')
        self.showMaximized()

        # Layout principal
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        # Layout superior com o relógio no canto direito
        topBar = QHBoxLayout()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setStyleSheet("color: white; font-size: 40px; padding: 10px;")
        topBar.addWidget(self.label)

        # Adicionar tarja preta
        topBarWidget = QWidget()
        topBarWidget.setLayout(topBar)
        topBarWidget.setFixedHeight(80)  # Altura ajustada da tarja preta
        topBarWidget.setStyleSheet("background-color: black;")
        mainLayout.addWidget(topBarWidget)

        # Layout central para o botão
        centerLayout = QVBoxLayout()
        centerLayout.addStretch()  # Adiciona espaço flexível acima do botão
        self.button = QPushButton('MENU', self)
        self.button.setStyleSheet("""
            background-color: #5E9CD3; color: white; font-size: 24px;
            border-radius: 15px; padding: 50px 50px;  # Botão quadrado um pouco maior
        """)
        self.button.clicked.connect(self.toggle)
        centerLayout.addWidget(self.button, alignment=Qt.AlignCenter)
        centerLayout.addStretch()  # Adiciona espaço flexível abaixo do botão

        mainLayout.addLayout(centerLayout)

        # Configurar o fundo da janela
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Window, QColor('#003366'))  # Azul mais suave
        self.setPalette(p)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.showTime()

    def toggle(self):
        if self.button.text() == 'MENU':
            self.button.setText('HOME')
            self.button.setStyleSheet("""
                background-color: black; color: #5E9CD3; font-size: 24px;
                border-radius: 15px; padding: 50px 50px;  # Botão quadrado um pouco maior
            """)
            p = self.palette()
            p.setColor(QPalette.Window, QColor('#5E9CD3'))  # Azul suave
            self.setPalette(p)
        else:
            self.button.setText('MENU')
            self.button.setStyleSheet("""
                background-color: #5E9CD3; color: white; font-size: 24px;
                border-radius: 15px; padding: 50px 50px;  # Botão quadrado um pouco maior
            """)
            p = self.palette()
            p.setColor(QPalette.Window, QColor('#003366'))  # Preto
            self.setPalette(p)

    def showTime(self):
        currentTime = QTime.currentTime().toString('HH:mm:ss')
        self.label.setText(currentTime)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
