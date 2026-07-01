#!/usr/bin/env python3
"""
Gerenciamento de configurações do GDANT.

Este módulo é responsável por carregar e salvar as configurações da aplicação
de forma persistente, garantindo que as últimas configurações sejam lembradas.
"""

import json
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class Config:
    """
    Classe para gerenciar as configurações da aplicação.
    
    Esta classe segue o padrão de configuração e não contém lógica de negócio,
    apenas persistência de dados. Todas as operações são delegadas para
    componentes especializados.
    """
    template: str = ""
    manual: str = ""
    input: str = ""
    output: str = ""
    generate_docx: bool = True
    generate_pdf: bool = True
    
    def __post_init__(self):
        """
        Inicializar o caminho do arquivo de configuração.
        """
        self.config_file = Path("config/config.json")
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load(self):
        """
        Carregar configurações do arquivo JSON.
        
        Se o arquivo não existir, as configurações padrão são mantidas.
        Se houver erro na leitura, o erro é registrado mas a aplicação
        continua com as configurações padrão.
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if hasattr(self, key):
                            setattr(self, key, value)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Erro ao carregar configurações: {e}")
    
    def save(self):
        """
        Salvar configurações no arquivo JSON.
        
        Se houver erro na escrita, o erro é registrado mas a aplicação
        continua funcionando.
        """
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(asdict(self), f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Erro ao salvar configurações: {e}")
