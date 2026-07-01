#!/usr/bin/env python3
"""
Extractores especializados para extração de dados de Processos Administrativos.

Este módulo contém funções de extração simples e independentes.
Cada função extrai um tipo específico de informação do texto bruto.

Não contém classes, regras de negócio complexas ou lógica de parsing.
"""

from __future__ import annotations

import re


def extract_process_number(text: str) -> str:
    """
    Extrai número do processo administrativo do texto.
    
    Formatos esperados:
    - 047799/2025-64
    - 060367/2025-49
    - 060561/2025-24
    
    Prioriza ocorrências próximas a "Processo nº", "SEI" ou "Referência: Processo nº".
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Número do processo encontrado ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Padrão: 6 dígitos / 4 dígitos - 2 dígitos
    pattern = r"\d{6}/\d{4}-\d{2}"
    
    # Buscar próximo a palavras-chave (melhor resultado)
    keywords = ["processo nº", "sei", "referência"]
    for keyword in keywords:
        # Buscar a palavra-chave e depois o padrão
        regex = rf"{keyword}[:\s]*({pattern})"
        match = re.search(regex, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    # Fallback: buscar o padrão em qualquer lugar
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    
    return ""


def extract_infraction_number(text: str) -> str:
    """
    Extrai número do Auto de Infração do texto.
    
    Formatos esperados:
    - 30697/25
    - 36839/25
    - 36891/25
    
    Prioriza ocorrências próximas a "Auto de Infração".
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Número da infração encontrado ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Padrão: 5 dígitos / 2 dígitos
    pattern = r"\d{5}/\d{2}"
    
    # Buscar próximo a "Auto de Infração" (melhor resultado)
    regex = rf"auto\s+de\s+infração[:\s]*({pattern})"
    match = re.search(regex, text, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # Fallback: buscar o padrão próximo a "Infração"
    regex = rf"infração[:\s]*({pattern})"
    match = re.search(regex, text, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # Fallback: buscar o padrão em qualquer lugar
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    
    return ""


def extract_cpf_cnpj(text: str) -> str:
    """
    Extrai CPF ou CNPJ do texto.
    
    Formatos esperados:
    - CPF: 123.456.789-00 ou 12345678900
    - CNPJ: 12.345.678/0001-95 ou 12345678000195
    
    Prioriza CNPJ quando ambos são encontrados.
    Tenta preservar formatação original quando possível.
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        CPF ou CNPJ encontrado ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Padrão CNPJ formatado: XX.XXX.XXX/XXXX-XX
    cnpj_formatted = r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}"
    match = re.search(cnpj_formatted, text)
    if match:
        return match.group(0)
    
    # Padrão CNPJ sem formatação: 14 dígitos
    cnpj_unformatted = r"\b\d{14}\b"
    match = re.search(cnpj_unformatted, text)
    if match:
        value = match.group(0)
        # Validar se tem pelo menos 14 dígitos consecutivos
        if len(value) == 14:
            return value
    
    # Padrão CPF formatado: XXX.XXX.XXX-XX
    cpf_formatted = r"\d{3}\.\d{3}\.\d{3}-\d{2}"
    match = re.search(cpf_formatted, text)
    if match:
        return match.group(0)
    
    # Padrão CPF sem formatação: 11 dígitos
    cpf_unformatted = r"\b\d{11}\b"
    match = re.search(cpf_unformatted, text)
    if match:
        value = match.group(0)
        # Validar se tem exatamente 11 dígitos
        if len(value) == 11:
            return value
    
    return ""
