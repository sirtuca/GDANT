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


# ============================================================================
# PADRÕES CENTRALIZADOS PARA REUTILIZAÇÃO
# ============================================================================

CEP_PATTERN = r"\d{5}-\d{3}|\d{8}"
"""Padrão para CEP: XXXXX-XXX ou XXXXXXXX"""

PHONE_PATTERN = r"\(?(?:\d{2})\)?[\s\.-]?9?\d{4}[\s\.-]?\d{4}"
"""Padrão para telefone: (XX) XXXXX-XXXX ou variações"""

EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
"""Padrão para email: user@domain.ext"""


# ============================================================================
# EXTRACTORES SPRINT 7.1 - DADOS DO CONTRIBUINTE
# ============================================================================

def extract_name(text: str) -> str:
    """
    Extrai nome do contribuinte do texto.
    
    Busca próximo a palavras-chave como "Contribuinte:", "Requerente:", "Nome:".
    Espera que o nome venha após a palavra-chave na mesma linha.
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Nome do contribuinte ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Palavras-chave típicas em processos administrativos
    keywords = ["contribuinte", "requerente", "razão social", "nome"]
    
    for keyword in keywords:
        # Buscar a palavra-chave seguida de dois-pontos e depois o nome
        # Captura tudo até fim da linha ou próxima quebra
        pattern = rf"{keyword}[:\s]+([A-Za-zÀ-ÿ\s]+?)(?:\n|$|[0-9])"
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            name = match.group(1).strip()
            if name and len(name) > 2:  # Validar nome não vazio e com tamanho mínimo
                return name
    
    return ""


def extract_logradouro(text: str) -> str:
    """
    Extrai logradouro (rua, avenida, etc) do texto.
    
    Busca padrões como "Rua", "Avenida", "Av.", "Praça", "Trav.", etc.
    Captura o nome do logradouro após o tipo.
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Logradouro ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Buscar tipos de logradouros comuns
    # Captura tipo + nome (até vírgula, quebra ou número)
    pattern = r"(?:Rua|Avenida|Av\.|Av|Praça|Pça|Trav\.|Travessa|Alameda|Estrada|Rod\.|Rodovia|Passagem|Beco|Viela|Quadra|Lote)\s+([A-Za-zÀ-ÿ\s\.]+?)(?:,|$|\n|\d)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        logradouro = match.group(1).strip()
        if logradouro:
            return logradouro
    
    return ""


def extract_numero(text: str) -> str:
    """
    Extrai número do endereço do texto.
    
    Busca número após "nº", "nº.", "número" ou similar.
    Aceita números simples ou com complementos como "123 A" ou "123-A".
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Número do endereço ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Buscar padrões: "nº 123", "número 456", "n. 789", etc
    pattern = r"(?:nº|n°|número|n\.)\s*([0-9]+(?:\s*[-/]?\s*[A-Za-z0-9]*)?)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        numero = match.group(1).strip()
        if numero:
            return numero
    
    return ""


def extract_complemento(text: str) -> str:
    """
    Extrai complemento do endereço do texto.
    
    Busca padrões como "Apto", "Sala", "Bloco", "Lote", etc.
    Captura o complemento após a palavra-chave.
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Complemento do endereço ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Buscar complementos típicos
    pattern = r"(?:Apto|Apt\.|Apartamento|Sala|Bloco|Lote|Edifício|Ed\.|Conj\.|Conjunto)\s+([A-Za-z0-9\s\-\.]*?)(?:,|$|\n|CEP)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        complemento = match.group(1).strip()
        if complemento:
            return complemento
    
    return ""


def extract_bairro(text: str) -> str:
    """
    Extrai bairro do texto.
    
    Busca próximo a palavras-chave como "Bairro:", "Bairro de", "Distrito:".
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Bairro ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Buscar "Bairro: " ou "Bairro de " ou "Distrito:"
    pattern = r"(?:Bairro|Distrito)[:\s]+([A-Za-zÀ-ÿ\s]+?)(?:,|$|\n)"
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if match:
        bairro = match.group(1).strip()
        if bairro:
            return bairro
    
    return ""


def extract_municipio(text: str) -> str:
    """
    Extrai município/cidade do texto.
    
    Busca próximo a palavras-chave como "Cidade:", "Município:", "Localidade:".
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Município ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Buscar "Cidade:", "Município:", "Localidade:", etc
    pattern = r"(?:Cidade|Município|Localidade)[:\s]+([A-Za-zÀ-ÿ\s]+?)(?:,|$|\n)"
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if match:
        municipio = match.group(1).strip()
        if municipio:
            return municipio
    
    return ""


def extract_uf(text: str) -> str:
    """
    Extrai UF (Unidade Federativa/Estado) do texto.
    
    Busca siglas de estado como "SP", "RJ", "MG", etc.
    Pode estar após "UF:", "Estado:", ou próximo a um CEP.
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        UF (2 letras maiúsculas) ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Lista de UFs válidas brasileiras
    ufs_validas = {
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    }
    
    # Padrão 1: UF após palavra-chave "UF:", "Estado:"
    pattern = r"(?:UF|Estado)[:\s]+([A-Z]{2})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        uf = match.group(1).upper()
        if uf in ufs_validas:
            return uf
    
    # Padrão 2: UF isolado antes de CEP
    pattern = r"\b([A-Z]{2})\s*[-,]?\s*" + CEP_PATTERN
    match = re.search(pattern, text)
    if match:
        uf = match.group(1).upper()
        if uf in ufs_validas:
            return uf
    
    return ""


def extract_cep(text: str) -> str:
    """
    Extrai CEP do texto.
    
    Suporta formatos: XXXXX-XXX ou XXXXXXXX
    Busca próximo a palavras-chave ou padrão isolado.
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        CEP ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Padrão: XXXXX-XXX ou XXXXXXXX
    pattern = CEP_PATTERN
    
    # Buscar próximo a palavras-chave (melhor resultado)
    keywords = ["cep", "cep:"]
    for keyword in keywords:
        regex = rf"{keyword}[:\s]*({pattern})"
        match = re.search(regex, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    # Fallback: buscar o padrão em qualquer lugar
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    
    return ""


def extract_telefone(text: str) -> str:
    """
    Extrai telefone do texto.
    
    Suporta formatos:
    - (XX) XXXXX-XXXX (celular)
    - (XX) XXXX-XXXX (fixo)
    - XX XXXXX-XXXX
    - XX XXXX-XXXX
    - (XX) 9XXXX-XXXX
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Telefone ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Padrão para telefone
    pattern = PHONE_PATTERN
    
    # Buscar próximo a palavras-chave (melhor resultado)
    keywords = ["telefone", "fone", "tel", "celular", "mobile", "whatsapp"]
    for keyword in keywords:
        regex = rf"{keyword}[:\s]*({pattern})"
        match = re.search(regex, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    # Fallback: buscar o padrão em qualquer lugar
    match = re.search(pattern, text)
    if match:
        return match.group(0).strip()
    
    return ""


def extract_email(text: str) -> str:
    """
    Extrai email do texto.
    
    Busca padrão de email: user@domain.ext
    Busca próximo a palavras-chave quando possível.
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Email ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Padrão para email
    pattern = EMAIL_PATTERN
    
    # Buscar próximo a palavras-chave (melhor resultado)
    keywords = ["email", "e-mail", "mail", "correio eletrônico"]
    for keyword in keywords:
        regex = rf"{keyword}[:\s]*({pattern})"
        match = re.search(regex, text, re.IGNORECASE)
        if match:
            return match.group(1).lower()
    
    # Fallback: buscar o padrão em qualquer lugar
    match = re.search(pattern, text)
    if match:
        return match.group(0).lower()
    
    return ""
