#!/usr/bin/env python3
"""
Modelos de dados para o GDANT.

Este módulo contém apenas estruturas de dados que representam
os domínios do negócio. Não contém lógica de processamento,
geração de documentos ou regras de negócio.
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
    Serve como contrato entre o parser e o gerador de documentos.
    """
    
    # Fonte
    source_pdf: Path | None = None
    """Caminho do arquivo PDF de origem"""
    
    raw_text: str = ""
    """Texto bruto extraído do PDF"""
    
    # Identificação do Processo
    process_number: str = ""
    """Número do processo administrativo"""
    
    infraction_number: str = ""
    """Número da notificação de infração"""
    
    judgment_notification_number: str = ""
    """Número da notificação do julgamento ao contribuinte"""
    
    # Dados do Contribuinte
    taxpayer_name: str = ""
    """Nome completo do contribuinte"""
    
    cpf_cnpj: str = ""
    """CPF ou CNPJ do contribuinte"""
    
    phone: str = ""
    """Telefone de contato do contribuinte"""
    
    email: str = ""
    """Email do contribuinte"""
    
    # Endereço
    address: str = ""
    """Endereço completo do contribuinte"""
    
    city: str = ""
    """Cidade"""
    
    state: str = ""
    """UF (estado)"""
    
    zip_code: str = ""
    """CEP"""
    
    # Datas
    notification_date: str = ""
    """Data da notificação (formato: DD/MM/YYYY)"""
    
    judgment_date: str = ""
    """Data do julgamento (formato: DD/MM/YYYY)"""
    
    judgment_notification_date: str = ""
    """Data de notificação do julgamento (formato: DD/MM/YYYY)"""
    
    ar_number: str = ""
    """Número do Aviso de Recebimento (AR) postal"""
    
    # Dados Financeiros
    debt_amount: Decimal = Decimal("0.0")
    """Valor da dívida em reais"""
    
    # Listas
    legal_basis: list[str] = field(default_factory=list)
    """Lista de fundamentos legais da inscrição"""
    
    observations: list[str] = field(default_factory=list)
    """Lista de observações adicionais do processo"""
