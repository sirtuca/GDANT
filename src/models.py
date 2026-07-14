#!/usr/bin/env python3
"""
Modelos de dados para o GDANT.

Este módulo contém apenas estruturas de dados que representam
os domínios do negócio. Não contém lógica de processamento,
geração de documentos ou regras de negócio.

ProcessData é o contrato oficial entre Parser e WordGenerator.
Cada campo mapeia diretamente para um placeholder do Template Mestre
ou é um campo interno necessário para processamento.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path


@dataclass
class ProcessData:
    """
    Dados de um Processo Administrativo após parsing.
    
    Representa um processo individual extraído de um PDF de Processo Administrativo.
    Serve como contrato oficial entre o parser e o gerador de documentos.
    
    REGRA: Cada campo deve satisfazer UMA destas condições:
    1. Mapeia diretamente para um placeholder do Template Mestre
    2. É um campo interno necessário para processamento
    
    Nenhuma duplicação de representação é permitida.
    """
    
    # ==================== CAMPOS INTERNOS ====================
    # Necessários para processamento, não mapeiam para placeholders
    
    source_pdf: Path | None = None
    """Caminho do arquivo PDF de origem"""
    
    raw_text: str = ""
    """Texto bruto extraído do PDF"""
    
    # ==================== PLACEHOLDERS DO TEMPLATE MESTRE ====================
    # Cada campo corresponde a um placeholder [PLACEHOLDER]
    
    # Identificação do Processo
    process_number: str = ""
    """Número do processo administrativo → [PROC]"""
    
    infraction_number: str = ""
    """Número da notificação de infração → [AI]"""
    
    # Identificação do Contribuinte
    nome: str = ""
    """Nome do contribuinte → [NOME]"""
    
    cpf_cnpj: str = ""
    """CPF ou CNPJ do contribuinte → [DOC]"""
    
    # Endereço do Contribuinte
    logradouro: str = ""
    """Logradouro (rua, avenida, etc) → [LOG]"""
    
    numero: str = ""
    """Número do endereço → [NR]"""
    
    complemento: str = ""
    """Complemento do endereço (apto, sala, etc) → [COMP]"""
    
    bairro: str = ""
    """Bairro → [BAIRRO]"""
    
    municipio: str = ""
    """Município/Cidade → [MUN]"""
    
    uf: str = ""
    """UF (Unidade Federativa/Estado) → [UF]"""
    
    cep: str = ""
    """CEP → [CEP]"""
    
    # Contato do Contribuinte
    telefone: str = ""
    """Telefone de contato → [FONE]"""
    
    email: str = ""
    """Email de contato → [EMAIL]"""
    
    # ==================== CAMPOS INTERNOS (PROCESSAMENTO) ====================
    # Necessários para processamento, não mapeiam para placeholders
    
    judgment_notification_number: str = ""
    """Número da notificação do julgamento ao contribuinte"""
    
    notification_date: str = ""
    """Data da notificação (formato: DD/MM/YYYY)"""
    
    judgment_date: str = ""
    """Data do julgamento (formato: DD/MM/YYYY)"""
    
    judgment_notification_date: str = ""
    """Data de notificação do julgamento (formato: DD/MM/YYYY)"""
    
    ar_number: str = ""
    """Número do Aviso de Recebimento (AR) postal"""
    
    debt_amount: Decimal = Decimal("0.0")
    """Valor da dívida em reais"""
    
    legal_basis: list[str] = field(default_factory=list)
    """Lista de fundamentos legais da inscrição"""
    
    observations: list[str] = field(default_factory=list)
    """Lista de observações adicionais do processo"""
