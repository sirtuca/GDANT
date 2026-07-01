#!/usr/bin/env python3
"""
GDANT - Gerador de Dívida Ativa

Aplicação para gerar Termos de Inscrição em Dívida Ativa a partir de
Processos Administrativos em PDF.
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from interface import MainWindow
from config import Config


def main():
    """
    Função principal da aplicação.
    """
    # Inicializar configurações
    config = Config()
    config.load()
    
    # Criar aplicação Qt
    app = QApplication(sys.argv)
    app.setApplicationName("GDANT")
    app.setApplicationVersion("0.1.0")
    
    # Criar e mostrar janela principal
    window = MainWindow(config)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
