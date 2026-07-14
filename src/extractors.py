#!/usr/bin/env python3
"""
Extractores especializados para extração de dados de Processos Administrativos.

Este módulo contém funções de extração simples e independentes.
Cada função extrai um tipo específico de informação do texto bruto.

Otimizado para Auto de Infração da Prefeitura Municipal de Campo Grande.
Padrões baseados na estrutura real do documento, não em heurísticas genéricas.
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

CEP_PATTERN = r"\d{5}-?\d{3}|\d{8}"
"""Padrão para CEP: XXXXX-XXX ou XXXXXXXX"""

PHONE_PATTERN = r"\d{4}-\d{4}|\d{5}-\d{4}|\(?(?:\d{2})\)?[\s\.-]?9?\d{4}[\s\.-]?\d{4}"
"""Padrão para telefone: XXXX-XXXX, XXXXX-XXXX ou variações com area"""


# ============================================================================
# EXTRACTORES SPRINT 7.1 - DADOS DO CONTRIBUINTE
# Baseados na estrutura real do Auto de Infração de Campo Grande
# ============================================================================

def extract_name(text: str) -> str:
    """
    Extrai nome do contribuinte do bloco CONTRIBUINTE.
    
    Estrutura no PDF:
    CONTRIBUINTE:
    26920100-2 LEONARDO COSTA LEITE DE SOUZA BENITES LT
    
    O número antes do nome é a inscrição municipal (outro campo).
    Captura tudo após o número até o fim da linha.
    
    Suporta nomes com punctuação, "&", "/", ".", commas, LTDA, ME, EIRELI, etc.
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Nome do contribuinte ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Procurar o bloco CONTRIBUINTE: seguido de número + nome
    # Padrão: CONTRIBUINTE: [número] [NOME até fim da linha]
    # Número: dígitos, hífen, dígitos
    # Nome: tudo após número até quebra de linha (permite punctuação, &, /, ., etc)
    pattern = r"CONTRIBUINTE:\s*\d+-\d+\s+(.+?)(?:\n|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if match:
        name = match.group(1).strip()
        if name and len(name) > 2:
            return name
    
    return ""


def extract_logradouro(text: str) -> str:
    """
    Extrai logradouro (rua, avenida, etc) do bloco de endereço.
    
    Estrutura no PDF:
    Endereço: RUA SPIPE CALARGE          1540 CEP: 79051560
    
    Captura tudo entre "Endereço:" e o número do endereço (que vem antes de CEP).
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Logradouro ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Procurar "Endereço:" seguido do logradouro até encontrar número + CEP
    # Padrão: Endereço: [LOGRADOURO] [NUMERO] CEP:
    pattern = r"Endereço:\s*([A-Z\sÀ-ÿ]+?)\s+\d+\s+CEP:"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        logradouro = match.group(1).strip()
        if logradouro:
            return logradouro
    
    return ""


def extract_numero(text: str) -> str:
    """
    Extrai número do endereço do bloco de endereço.
    
    Estrutura no PDF:
    Endereço: RUA SPIPE CALARGE          1540 CEP: 79051560
    
    Captura o número entre logradouro e "CEP:".
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Número do endereço ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Procurar número após logradouro, antes de CEP
    # Padrão: [LOGRADOURO] [NUMERO] CEP:
    pattern = r"Endereço:\s*[A-Z\sÀ-ÿ]+\s+(\d+)\s+CEP:"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        numero = match.group(1).strip()
        if numero:
            return numero
    
    return ""


def extract_complemento(text: str) -> str:
    """
    Extrai complemento do endereço (apto, sala, bloco, etc).
    
    Estrutura no PDF:
    Nem sempre presente. Se existir, vem após o número ou em linha separada.
    
    Como não há padrão claro no documento de exemplo, retorna string vazia.
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        String vazia (tolera ausência do complemento)
    """
    return ""


def extract_bairro(text: str) -> str:
    """
    Extrai bairro do bloco de endereço.
    
    Estrutura no PDF:
    Bairro: VILA CARLOTA
    
    Captura tudo até o fim da linha.
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Bairro ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Procurar "Bairro:" seguido do nome do bairro até fim da linha
    pattern = r"Bairro:\s*(.+?)(?:\n|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if match:
        bairro = match.group(1).strip()
        if bairro:
            return bairro
    
    return ""


def extract_municipio(text: str) -> str:
    """
    Extrai município APENAS se explicitamente declarado no PDF.
    
    TODO: O layout atual do Auto de Infração de Campo Grande não contém
    um campo explícito de "Município:" no bloco CONTRIBUINTE.
    Quando o padrão for identificado em outros documentos, atualizar
    esta função com uma regex confiável.
    
    Se não encontrado com confiança, retorna string vazia.
    Nunca usa defaults (ex: "Campo Grande").
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Município ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Procurar "Município:" ou "Cidade:"
    # (padrão não identificado no layout atual, mas preparado para futura expansão)
    pattern = r"(?:Município|Cidade)[:\s]+([A-Z\sÀ-ÿ]+?)(?:,|$|\n)"
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if match:
        municipio = match.group(1).strip()
        if municipio:
            return municipio
    
    return ""


def extract_uf(text: str) -> str:
    """
    Extrai UF (Unidade Federativa/Estado) APENAS se explicitamente declarada no PDF.
    
    Se não encontrada com confiança, retorna string vazia.
    Nunca usa defaults (ex: "MS").
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        UF (2 letras maiúsculas) ou string vazia se não encontrada
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
    
    # Se não encontrou, retorna vazio (sem default)
    return ""


def extract_cep(text: str) -> str:
    """
    Extrai CEP do bloco de endereço.
    
    Estrutura no PDF:
    Endereço: RUA SPIPE CALARGE          1540 CEP: 79051560
    
    Suporta formatos: XXXXX-XXX ou XXXXXXXX
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        CEP ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Procurar "CEP:" seguido do CEP
    pattern = rf"CEP:\s*({CEP_PATTERN})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        cep = match.group(1).strip()
        if cep:
            return cep
    
    return ""


def extract_telefone(text: str) -> str:
    """
    Extrai telefone do bloco de contato.
    
    Estrutura no PDF:
    Telefone: 9948-5836
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Telefone ou string vazia se não encontrado
    """
    if not text:
        return ""
    
    # Procurar "Telefone:" seguido do número
    pattern = rf"Telefone:\s*({PHONE_PATTERN})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        telefone = match.group(1).strip()
        if telefone:
            return telefone
    
    return ""


def extract_email(text: str) -> str:
    """
    Extrai email do texto.
    
    Nem sempre presente no Auto de Infração.
    Se não encontrado, retorna string vazia.
    
    Args:
        text: Texto bruto extraído do PDF
    
    Returns:
        Email ou string vazia se não encontrado
    """
    return ""
