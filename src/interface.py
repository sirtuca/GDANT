#!/usr/bin/env python3
"""
Interface gráfica do GDANT usando PySide6.

Este módulo implementa apenas a apresentação. Toda lógica de negócio
é delegada para o módulo engine. A interface é agnóstica em relação
à implementação do processamento.
"""

from __future__ import annotations

from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QProgressBar,
    QTextEdit,
    QFileDialog,
)
from PySide6.QtCore import Qt

from config import Config
from engine import ProcessingEngine


class MainWindow(QMainWindow):
    """
    Janela principal da aplicação GDANT.
    
    Responsável apenas pela apresentação e captura de eventos do usuário.
    Nenhuma lógica de negócio é implementada aqui.
    """
    
    def __init__(self, config: Config):
        """
        Inicializar a janela principal.
        
        Args:
            config: Objeto de configuração da aplicação
        """
        super().__init__()
        self.config = config
        self.engine = ProcessingEngine()
        
        self.setWindowTitle("GDANT - Gerador de Dívida Ativa")
        self.setGeometry(100, 100, 900, 700)
        
        self._create_ui()
        self._load_config_values()
    
    def _create_ui(self):
        """
        Criar a interface do usuário.
        
        Organiza os componentes em grupos temáticos para melhor UX.
        """
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Seção de Configurações
        config_group = self._create_config_group()
        main_layout.addWidget(config_group)
        
        # Seção de Opções de Saída
        options_group = self._create_options_group()
        main_layout.addWidget(options_group)
        
        # Botão de Ação
        button_layout = QHBoxLayout()
        self.btn_generate = QPushButton("GERAR TERMOS")
        self.btn_generate.setMinimumHeight(40)
        self.btn_generate.clicked.connect(self._on_generate_clicked)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_generate)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Barra de Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # Área de Status
        status_label = QLabel("Status:")
        main_layout.addWidget(status_label)
        
        self.status_area = QTextEdit()
        self.status_area.setReadOnly(True)
        self.status_area.setMinimumHeight(120)
        main_layout.addWidget(self.status_area)
        
        main_layout.addStretch()
    
    def _create_config_group(self) -> QGroupBox:
        """
        Criar grupo de configurações de pastas e arquivos.
        
        Returns:
            QGroupBox com os campos de configuração
        """
        group = QGroupBox("Configurações")
        layout = QVBoxLayout()
        
        # Template Mestre
        template_layout = QHBoxLayout()
        template_layout.addWidget(QLabel("Template Mestre:"))
        self.template_input = QLineEdit()
        self.template_input.setReadOnly(True)
        template_layout.addWidget(self.template_input)
        self.btn_template = QPushButton("Trocar")
        self.btn_template.clicked.connect(self._on_select_template)
        template_layout.addWidget(self.btn_template)
        layout.addLayout(template_layout)
        
        # Manual Técnico
        manual_layout = QHBoxLayout()
        manual_layout.addWidget(QLabel("Manual Técnico:"))
        self.manual_input = QLineEdit()
        self.manual_input.setReadOnly(True)
        manual_layout.addWidget(self.manual_input)
        self.btn_manual = QPushButton("Trocar")
        self.btn_manual.clicked.connect(self._on_select_manual)
        manual_layout.addWidget(self.btn_manual)
        layout.addLayout(manual_layout)
        
        # Pasta de Processos (Input)
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Pasta de Processos:"))
        self.input_folder = QLineEdit()
        self.input_folder.setReadOnly(True)
        input_layout.addWidget(self.input_folder)
        self.btn_input = QPushButton("Trocar")
        self.btn_input.clicked.connect(self._on_select_input_folder)
        input_layout.addWidget(self.btn_input)
        layout.addLayout(input_layout)
        
        # Pasta de Saída (Output)
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Pasta de Saída:"))
        self.output_folder = QLineEdit()
        self.output_folder.setReadOnly(True)
        output_layout.addWidget(self.output_folder)
        self.btn_output = QPushButton("Trocar")
        self.btn_output.clicked.connect(self._on_select_output_folder)
        output_layout.addWidget(self.btn_output)
        layout.addLayout(output_layout)
        
        group.setLayout(layout)
        return group
    
    def _create_options_group(self) -> QGroupBox:
        """
        Criar grupo de opções de saída.
        
        Returns:
            QGroupBox com as opções de geração
        """
        group = QGroupBox("Opções de Saída")
        layout = QHBoxLayout()
        
        self.checkbox_docx = QCheckBox("Gerar DOCX")
        self.checkbox_docx.setChecked(self.config.generate_docx)
        layout.addWidget(self.checkbox_docx)
        
        self.checkbox_pdf = QCheckBox("Gerar PDF")
        self.checkbox_pdf.setChecked(self.config.generate_pdf)
        layout.addWidget(self.checkbox_pdf)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
    
    def _load_config_values(self):
        """
        Carregar valores de configuração nos campos da interface.
        """
        self.template_input.setText(self.config.template)
        self.manual_input.setText(self.config.manual)
        self.input_folder.setText(self.config.input)
        self.output_folder.setText(self.config.output)
        self.checkbox_docx.setChecked(self.config.generate_docx)
        self.checkbox_pdf.setChecked(self.config.generate_pdf)
    
    def _save_config_values(self):
        """
        Salvar valores de configuração nos settings.
        """
        self.config.template = self.template_input.text()
        self.config.manual = self.manual_input.text()
        self.config.input = self.input_folder.text()
        self.config.output = self.output_folder.text()
        self.config.generate_docx = self.checkbox_docx.isChecked()
        self.config.generate_pdf = self.checkbox_pdf.isChecked()
        self.config.save()
    
    def _on_select_template(self):
        """
        Abrir diálogo para selecionar template mestre.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Template Mestre",
            self.config.template or "templates/",
            "Arquivos DOCX (*.docx);;Todos os Arquivos (*)"
        )
        if file_path:
            self.template_input.setText(file_path)
            self._save_config_values()
            self._update_status(f"Template selecionado: {file_path}")
    
    def _on_select_manual(self):
        """
        Abrir diálogo para selecionar manual técnico.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Manual Técnico",
            self.config.manual or "manuals/",
            "Arquivos PDF (*.pdf);;Todos os Arquivos (*)"
        )
        if file_path:
            self.manual_input.setText(file_path)
            self._save_config_values()
            self._update_status(f"Manual selecionado: {file_path}")
    
    def _on_select_input_folder(self):
        """
        Abrir diálogo para selecionar pasta de entrada.
        """
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Selecionar Pasta de Processos",
            self.config.input or "input/"
        )
        if folder_path:
            self.input_folder.setText(folder_path)
            self._save_config_values()
            self._update_status(f"Pasta de entrada selecionada: {folder_path}")
    
    def _on_select_output_folder(self):
        """
        Abrir diálogo para selecionar pasta de saída.
        """
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Selecionar Pasta de Saída",
            self.config.output or "output/"
        )
        if folder_path:
            self.output_folder.setText(folder_path)
            self._save_config_values()
            self._update_status(f"Pasta de saída selecionada: {folder_path}")
    
    def _on_generate_clicked(self):
        """
        Handler do botão GERAR TERMOS.
        
        Escaneia a pasta de entrada, encontra PDFs e exibe lista no log.
        """
        # Salvar configurações atuais
        self._save_config_values()
        
        # Validar campos
        if not self._validate_inputs():
            return
        
        self._update_status("Escaneando pasta de entrada...")
        self.progress_bar.setValue(0)
        self.btn_generate.setEnabled(False)
        
        try:
            # Escanear pasta de entrada
            input_path = Path(self.input_folder.text())
            scan_result = self.engine.scan_input_folder(input_path)
            
            # Atualizar barra de progresso com total de PDFs
            self.progress_bar.setMaximum(scan_result.total)
            self.progress_bar.setValue(scan_result.total)
            
            # Log inicial
            self._update_status(f"✓ Total de PDFs encontrados: {scan_result.total}")
            
            # Listar cada PDF no log
            for pdf_file in scan_result.pdf_files:
                self._update_status(f"  → {pdf_file.name}")
            
            if scan_result.total == 0:
                self._update_status("⚠ Nenhum arquivo PDF encontrado na pasta.")
            else:
                self._update_status("✓ Pronto para processar.")
        
        except ValueError as e:
            self._update_status(f"✗ Erro: {str(e)}")
            self.progress_bar.setValue(0)
        except Exception as e:
            self._update_status(f"✗ Erro inesperado: {str(e)}")
            self.progress_bar.setValue(0)
        finally:
            self.btn_generate.setEnabled(True)
    
    def _validate_inputs(self) -> bool:
        """
        Validar se os campos obrigatórios foram preenchidos.
        
        Returns:
            True se tudo está válido, False caso contrário
        """
        errors = []
        
        if not self.template_input.text():
            errors.append("Template Mestre não selecionado")
        
        if not self.input_folder.text():
            errors.append("Pasta de Processos não selecionada")
        
        if not self.output_folder.text():
            errors.append("Pasta de Saída não selecionada")
        
        if not self.checkbox_docx.isChecked() and not self.checkbox_pdf.isChecked():
            errors.append("Selecione pelo menos um formato de saída (DOCX ou PDF)")
        
        if errors:
            error_message = "Erros encontrados:\n" + "\n".join(f"• {error}" for error in errors)
            self._update_status(error_message)
            return False
        
        return True
    
    def _update_status(self, message: str):
        """
        Atualizar a área de status com uma mensagem.
        
        Args:
            message: Mensagem a ser exibida
        """
        self.status_area.append(message)
        # Rolar para o final do texto
        self.status_area.verticalScrollBar().setValue(
            self.status_area.verticalScrollBar().maximum()
        )
    
    def closeEvent(self, event):
        """
        Salvar configurações ao fechar a aplicação.
        
        Args:
            event: Evento de fechamento da janela
        """
        self._save_config_values()
        event.accept()
