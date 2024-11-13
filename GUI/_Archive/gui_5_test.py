import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Importe a classe MyApp do arquivo gui.py
from gui_5 import MyApp

# Variável para definir o número de toques
num_clicks = 10  # Defina o número de toques aqui

def test_button_click():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()

    button = window.getButton()
    
    # Imprime o texto do botão antes do clique
    print(f"Texto do botão antes do clique: {button.text()}")
    assert button.text() == "MENU"  # Verifica o estado inicial

    # Contadores para a métrica
    correct_clicks = 0

    # Loop para emular o clique múltiplas vezes
    for i in range(num_clicks):
        QTest.mouseClick(button, Qt.LeftButton)
        app.processEvents()
        
        # Imprime o texto do botão após cada clique
        print(f"Texto do botão após clique {i+1}: {button.text()}")
        
        # Verifica se o clique foi correto
        expected_text = "HOME" if (i + 1) % 2 == 1 else "MENU"
        if button.text() == expected_text:
            correct_clicks += 1
        
        time.sleep(1)
    
    # Verifica se o texto do botão mudou adequadamente após todos os cliques
    final_state = "HOME" if num_clicks % 2 == 1 else "MENU"
    assert button.text() == final_state
    
    # Calcula a porcentagem de acerto dos toques
    accuracy = (correct_clicks / num_clicks) * 100
    print(f"Porcentagem de acerto dos toques: {accuracy:.2f}%")

    # Aguarda um pouco para ver o resultado na GUI
    time.sleep(2)
    
    # Não fechar a aplicação imediatamente
    window.close()

if __name__ == '__main__':
    test_button_click()
