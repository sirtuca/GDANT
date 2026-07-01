#!/usr/bin/env python3
"""
Testes unitários para o módulo extractors.

Valida as funções de extração de dados de Processos Administrativos.
"""

from __future__ import annotations

from src.extractors import extract_cpf_cnpj, extract_infraction_number, extract_process_number


class TestExtractProcessNumber:
    """Testes para extract_process_number()."""

    def test_extract_process_number_success(self) -> None:
        """Deve extrair número do processo com palavra-chave."""
        text = "Processo nº 047799/2025-64"
        result = extract_process_number(text)
        assert result == "047799/2025-64"

    def test_extract_process_number_with_sei(self) -> None:
        """Deve extrair número do processo próximo a SEI."""
        text = "SEI: 060367/2025-49"
        result = extract_process_number(text)
        assert result == "060367/2025-49"

    def test_extract_process_number_with_referencia(self) -> None:
        """Deve extrair número do processo próximo a Referência."""
        text = "Referência: Processo nº 060561/2025-24"
        result = extract_process_number(text)
        assert result == "060561/2025-24"

    def test_extract_process_number_fallback(self) -> None:
        """Deve extrair número do processo sem palavra-chave."""
        text = "O documento 047799/2025-64 está anexado."
        result = extract_process_number(text)
        assert result == "047799/2025-64"

    def test_extract_process_number_not_found(self) -> None:
        """Deve retornar string vazia se processo não encontrado."""
        text = "Este texto não contém número de processo."
        result = extract_process_number(text)
        assert result == ""

    def test_extract_process_number_empty_text(self) -> None:
        """Deve retornar string vazia para texto vazio."""
        result = extract_process_number("")
        assert result == ""


class TestExtractInfractionNumber:
    """Testes para extract_infraction_number()."""

    def test_extract_infraction_number_success(self) -> None:
        """Deve extrair número da infração com palavra-chave."""
        text = "Auto de Infração 30697/25"
        result = extract_infraction_number(text)
        assert result == "30697/25"

    def test_extract_infraction_number_with_colon(self) -> None:
        """Deve extrair número da infração com dois pontos."""
        text = "Auto de Infração: 36839/25"
        result = extract_infraction_number(text)
        assert result == "36839/25"

    def test_extract_infraction_number_with_multiple_spaces(self) -> None:
        """Deve extrair número da infração com múltiplos espaços."""
        text = "Auto  de  Infração  36891/25"
        result = extract_infraction_number(text)
        assert result == "36891/25"

    def test_extract_infraction_number_fallback(self) -> None:
        """Deve extrair número da infração sem palavra-chave."""
        text = "A notificação 30697/25 foi emitida."
        result = extract_infraction_number(text)
        assert result == "30697/25"

    def test_extract_infraction_number_not_found(self) -> None:
        """Deve retornar string vazia se infração não encontrada."""
        text = "Este texto não contém número de infração."
        result = extract_infraction_number(text)
        assert result == ""

    def test_extract_infraction_number_empty_text(self) -> None:
        """Deve retornar string vazia para texto vazio."""
        result = extract_infraction_number("")
        assert result == ""


class TestExtractCpfCnpj:
    """Testes para extract_cpf_cnpj()."""

    def test_extract_cnpj_formatted(self) -> None:
        """Deve extrair CNPJ formatado."""
        text = "CNPJ 12.345.678/0001-95"
        result = extract_cpf_cnpj(text)
        assert result == "12.345.678/0001-95"

    def test_extract_cnpj_formatted_priority(self) -> None:
        """Deve priorizar CNPJ quando ambos existem."""
        text = "CNPJ 12.345.678/0001-95 e CPF 123.456.789-00"
        result = extract_cpf_cnpj(text)
        assert result == "12.345.678/0001-95"

    def test_extract_cnpj_unformatted(self) -> None:
        """Deve extrair CNPJ sem formatação."""
        text = "CNPJ: 12345678000195"
        result = extract_cpf_cnpj(text)
        assert result == "12345678000195"

    def test_extract_cpf_formatted(self) -> None:
        """Deve extrair CPF formatado."""
        text = "CPF 123.456.789-00"
        result = extract_cpf_cnpj(text)
        assert result == "123.456.789-00"

    def test_extract_cpf_formatted_with_label(self) -> None:
        """Deve extrair CPF formatado com rótulo."""
        text = "O CPF do contribuinte é 987.654.321-00"
        result = extract_cpf_cnpj(text)
        assert result == "987.654.321-00"

    def test_extract_cpf_unformatted(self) -> None:
        """Deve extrair CPF sem formatação."""
        text = "CPF: 12345678900"
        result = extract_cpf_cnpj(text)
        assert result == "12345678900"

    def test_extract_cpf_cnpj_not_found(self) -> None:
        """Deve retornar string vazia se CPF/CNPJ não encontrado."""
        text = "Este texto não contém CPF ou CNPJ."
        result = extract_cpf_cnpj(text)
        assert result == ""

    def test_extract_cpf_cnpj_empty_text(self) -> None:
        """Deve retornar string vazia para texto vazio."""
        result = extract_cpf_cnpj("")
        assert result == ""

    def test_extract_cpf_cnpj_invalid_length(self) -> None:
        """Deve ignorar números que não correspondem a CPF/CNPJ."""
        text = "Número 123456 não é CPF nem CNPJ"
        result = extract_cpf_cnpj(text)
        assert result == ""

    def test_extract_cpf_cnpj_in_context(self) -> None:
        """Deve extrair CPF em contexto com outro texto."""
        text = (
            "Contribuinte: João Silva\n"
            "CPF: 123.456.789-00\n"
            "Endereço: Rua das Flores, 123"
        )
        result = extract_cpf_cnpj(text)
        assert result == "123.456.789-00"
