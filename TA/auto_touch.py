import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtCore import Qt, QPoint, QEvent, QTimer
import time

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton('Clique aqui', self)
        self.button.clicked.connect(self.next_screen)

        self.reset_button = QPushButton('Resetar', self)
        self.reset_button.clicked.connect(self.reset_and_continue)
        self.reset_button.hide()

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Minha Janela PyQt')

        self.iteration = 0
        self.results = []

    def next_screen(self):
        self.setStyleSheet("background-color: blue;")
        self.button.hide()
        self.reset_button.show()

    def simulate_click(self):
        # Simula um clique no centro do botão
        rect = self.button.geometry()
        x = rect.x() + rect.width() // 2
        y = rect.y() + rect.height() // 2

        # Cria um evento de clique do mouse
        mouse_event = QMouseEvent(QEvent.MouseButtonPress, 
                                  QPoint(x, y), 
                                  Qt.LeftButton,
                                  Qt.LeftButton,
                                  Qt.NoModifier)

        # Envia o evento para o botão
        QApplication.postEvent(self.button, mouse_event)

        QTimer.singleShot(100, self.simulate_release_click)

    def simulate_release_click(self):
        # Simula a liberação do clique no centro do botão
        rect = self.button.geometry()
        x = rect.x() + rect.width() // 2
        y = rect.y() + rect.height() // 2

        # Cria um evento de liberação do mouse para completar o clique
        mouse_event_release = QMouseEvent(QEvent.MouseButtonRelease, 
                                          QPoint(x, y), 
                                          Qt.LeftButton, 
                                          Qt.LeftButton, 
                                          Qt.NoModifier)
        QApplication.postEvent(self.button, mouse_event_release)

        # Adiciona um pequeno atraso antes de coletar o resultado
        QTimer.singleShot(100, self.collect_results)

        # Simula o clique no botão "Resetar" após um pequeno atraso
        QTimer.singleShot(100, self.simulate_reset_click)

    def collect_results(self):
        self.results.append('success' if self.button.isHidden() or self.reset_button.isVisible() else 'failure')

    def simulate_reset_click(self):
        # Simula um clique no centro do botão "Resetar"
        rect = self.reset_button.geometry()
        x = rect.x() + rect.width() // 2
        y = rect.y() + rect.height() // 2

        # Cria um evento de clique do mouse
        mouse_event = QMouseEvent(QEvent.MouseButtonPress, 
                                  QPoint(x, y), 
                                  Qt.LeftButton, 
                                  Qt.LeftButton, 
                                  Qt.NoModifier)

        # Envia o evento para o botão
        QApplication.postEvent(self.reset_button, mouse_event)

        # Cria um QTimer para simular a liberação do clique após um pequeno atraso
        QTimer.singleShot(100, self.simulate_reset_release_click)

    def simulate_reset_release_click(self):
        # Simula a liberação do clique no centro do botão "Resetar"
        rect = self.reset_button.geometry()
        x = rect.x() + rect.width() // 2
        y = rect.y() + rect.height() // 2

        # Cria um evento de liberação do mouse
        mouse_event_release = QMouseEvent(QEvent.MouseButtonRelease, 
                                          QPoint(x, y), 
                                          Qt.LeftButton, 
                                          Qt.LeftButton, 
                                          Qt.NoModifier)
        # Envia o evento para o botão
        QApplication.postEvent(self.reset_button, mouse_event_release)

        # Incrementa o contador de iterações
        self.iteration += 1

        # Verifica se deve continuar o loop
        if self.iteration < 50:
            self.reset_and_continue()
        else:
            print("Resultados:", self.results)
            self.get_results()

    def reset_and_continue(self):
        # Reseta a interface para a próxima iteração
        self.setStyleSheet("")
        self.button.show()
        self.reset_button.hide()

        # Processa eventos pendentes para garantir que a interface seja atualizada
        QApplication.processEvents()

        # Cria um QTimer para iniciar a próxima iteração após um pequeno atraso
        QTimer.singleShot(100, self.simulate_click)

    def get_results(self):
        success = self.results.count('success')
        failure = self.results.count('failure')
        if success and failure:
            success_rate = success/len(self.results)*100
            failure_rate = failure/len(self.results)*100
            print(f"Success rate: {success_rate}\nFailure rate: {failure_rate}")
            sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()

    # Cria um QTimer para simular o clique
    QTimer.singleShot(500, window.simulate_click)

    results = window.get_results()
    print(results)

    sys.exit(app.exec_())
