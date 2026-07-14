#!/usr/bin/env python3
"""
Parser para extração e assembla de ProcessData a partir de texto bruto.

Este módulo coordena os extractors para montar a estrutura ProcessData.
Tolera dados faltando na primeira versão.
"""

from __future__ import annotations

from pathlib import Path

from src.extractors import (
    extract_cpf_cnpj,
    extract_infraction_number,
    extract_process_number,
    extract_name,
    extract_logradouro,
    extract_numero,
    extract_complemento,
    extract_bairro,
    extract_municipio,
    extract_uf,
    extract_cep,
    extract_telefone,
    extract_email,
)
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
        # Extrair dados usando extractors - Campos existentes
        
        print("\n[PARSER] Iniciando extração de process_number...")
        process_number = extract_process_number(text)
        print(f"[PARSER] ✓ process_number extraído: {process_number}")
        
        print("\n[PARSER] Iniciando extração de infraction_number...")
        infraction_number = extract_infraction_number(text)
        print(f"[PARSER] ✓ infraction_number extraído: {infraction_number}")
        
        print("\n[PARSER] Iniciando extração de cpf_cnpj...")
        cpf_cnpj = extract_cpf_cnpj(text)
        print(f"[PARSER] ✓ cpf_cnpj extraído: {cpf_cnpj}")
        
        # Extrair dados usando extractors - Novos campos Sprint 7.1
        
        print("\n[PARSER] Iniciando extração de nome...")
        nome = extract_name(text)
        print(f"[PARSER] ✓ nome extraído: {nome}")
        
        print("\n[PARSER] Iniciando extração de logradouro...")
        logradouro = extract_logradouro(text)
        print(f"[PARSER] ✓ logradouro extraído: {logradouro}")
        
        print("\n[PARSER] Iniciando extração de numero...")
        numero = extract_numero(text)
        print(f"[PARSER] ✓ numero extraído: {numero}")
        
        print("\n[PARSER] Iniciando extração de complemento...")
        complemento = extract_complemento(text)
        print(f"[PARSER] ✓ complemento extraído: {complemento}")
        
        print("\n[PARSER] Iniciando extração de bairro...")
        bairro = extract_bairro(text)
        print(f"[PARSER] ✓ bairro extraído: {bairro}")
        
        print("\n[PARSER] Iniciando extração de municipio...")
        municipio = extract_municipio(text)
        print(f"[PARSER] ✓ municipio extraído: {municipio}")
        
        print("\n[PARSER] Iniciando extração de uf...")
        uf = extract_uf(text)
        print(f"[PARSER] ✓ uf extraído: {uf}")
        
        print("\n[PARSER] Iniciando extração de cep...")
        cep = extract_cep(text)
        print(f"[PARSER] ✓ cep extraído: {cep}")
        
        print("\n[PARSER] Iniciando extração de telefone...")
        telefone = extract_telefone(text)
        print(f"[PARSER] ✓ telefone extraído: {telefone}")
        
        print("\n[PARSER] Iniciando extração de email...")
        email = extract_email(text)
        print(f"[PARSER] ✓ email extraído: {email}")
        
        # Montar ProcessData com dados extraídos
        print("\n[PARSER] Montando ProcessData com todos os campos...")
        process_data = ProcessData(
            source_pdf=source_pdf,
            raw_text=text,
            process_number=process_number,
            infraction_number=infraction_number,
            cpf_cnpj=cpf_cnpj,
            nome=nome,
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            municipio=municipio,
            uf=uf,
            cep=cep,
            telefone=telefone,
            email=email,
        )
        print("[PARSER] ✓ ProcessData montado com sucesso!\n")
        
        return process_data
