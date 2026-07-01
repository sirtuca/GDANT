#!/usr/bin/env python3
"""
Configuração de estado da aplicação GDANT.

Gerencia preferências de usuário, caminhos de arquivos e opções de geração.
NÃO confundir com src/config.py que contém constantes globais do sistema (OCR, etc).

Responsabilidades:
- Caminhos de templates e manuais
- Pasta de entrada/saída
- Opções de geração (DOCX, PDF)
- Persistência de configurações em disco
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional
import json


class AppConfig:
    """
    Configuração de estado da aplicação.
    
    Gerencia caminhos de arquivo, preferências de UI e opções de geração.
    Persiste valores em arquivo JSON para recuperação entre sessões.
    """
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Inicializar configuração da aplicação.
        
        Args:
            config_file: Caminho do arquivo de configuração JSON.
                        Se None, usa "config/app_settings.json"
        """
        if config_file is None:
            config_file = Path("config") / "app_settings.json"
        
        self.config_file = config_file
        
        # Valores padrão
        self.template: str = ""
        self.manual: str = ""
        self.input: str = ""
        self.output: str = ""
        self.generate_docx: bool = True
        self.generate_pdf: bool = False
        
        # Tentar carregar configuração salva
        self.load()
    
    def load(self) -> None:
        """
        Carregar configuração do arquivo JSON.
        
        Se o arquivo não existir, mantém valores padrão.
        """
        if not self.config_file.exists():
            return
        
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.template = data.get("template", "")
            self.manual = data.get("manual", "")
            self.input = data.get("input", "")
            self.output = data.get("output", "")
            self.generate_docx = data.get("generate_docx", True)
            self.generate_pdf = data.get("generate_pdf", False)
        
        except Exception as e:
            print(f"[APPCONFIG] Aviso: Não foi possível carregar configuração: {e}")
    
    def save(self) -> None:
        """
        Salvar configuração em arquivo JSON.
        
        Cria o diretório se não existir.
        """
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "template": self.template,
                "manual": self.manual,
                "input": self.input,
                "output": self.output,
                "generate_docx": self.generate_docx,
                "generate_pdf": self.generate_pdf,
            }
            
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            print(f"[APPCONFIG] Erro ao salvar configuração: {e}")
