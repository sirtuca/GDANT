#!/usr/bin/env python3
"""
Parser para extração e assembla de ProcessData a partir de texto bruto.

Este módulo coordena os extractors para montar a estrutura ProcessData.
Tolera dados faltando na primeira versão.
"""

from __future__ import annotations

from pathlib import Path

from src.extractors import extract_cpf_cnpj, extract_infraction_number, extract_process_number
from src.models import ProcessData


class ParseError(Exception):
    """Erro durante o parsing de texto."""

    pass


class Parser:
    """
    Parser que monta ProcessData a partir de texto bruto de PDF.
    
    Coordena extractors e assembla a estrutura de dados contratual.
    Na primeira versão, tolera dados faltando sem lançar exceções.
    """

    def parse(self, text: str, source_pdf: Path | None = None) -> ProcessData:
        """
        Parse de texto bruto e retorna ProcessData.
        
        Coordena os extractors para preencher os campos do ProcessData.
        Tolera campos não encontrados (retorna strings vazias).
        
        Args:
            text: Texto bruto extraído do PDF
            source_pdf: Caminho do arquivo PDF de origem (opcional)
        
        Returns:
            ProcessData preenchido com dados extraídos
        """
        # Extrair dados usando extractors
        process_number = extract_process_number(text)
        infraction_number = extract_infraction_number(text)
        cpf_cnpj = extract_cpf_cnpj(text)
        
        # Montar ProcessData com dados extraídos
        process_data = ProcessData(
            source_pdf=source_pdf,
            raw_text=text,
            process_number=process_number,
            infraction_number=infraction_number,
            cpf_cnpj=cpf_cnpj,
        )
        
        return process_data
