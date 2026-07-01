#!/usr/bin/env python3
"""
Testes unitários para o módulo parser.

Valida a classe Parser e sua capacidade de montar ProcessData.
"""

from __future__ import annotations

from pathlib import Path

from src.parser import Parser
from src.models import ProcessData


class TestParser:
    """Testes para a classe Parser."""

    def test_parse_complete_text(self) -> None:
        """Deve extrair todos os campos quando presentes."""
        text = (
            "Processo nº 047799/2025-64\n"
            "Auto de Infração 30697/25\n"
            "CNPJ 12.345.678/0001-95"
        )
        parser = Parser()
        result = parser.parse(text)
        
        assert isinstance(result, ProcessData)
        assert result.process_number == "047799/2025-64"
        assert result.infraction_number == "30697/25"
        assert result.cpf_cnpj == "12.345.678/0001-95"
        assert result.raw_text == text

    def test_parse_partial_text(self) -> None:
        """Deve retornar ProcessData mesmo com dados faltando."""
        text = "Processo nº 060367/2025-49"
        parser = Parser()
        result = parser.parse(text)
        
        assert isinstance(result, ProcessData)
        assert result.process_number == "060367/2025-49"
        assert result.infraction_number == ""
        assert result.cpf_cnpj == ""
        assert result.raw_text == text

    def test_parse_empty_text(self) -> None:
        """Deve retornar ProcessData com campos vazios para texto vazio."""
        parser = Parser()
        result = parser.parse("")
        
        assert isinstance(result, ProcessData)
        assert result.process_number == ""
        assert result.infraction_number == ""
        assert result.cpf_cnpj == ""
        assert result.raw_text == ""

    def test_parse_with_source_pdf(self) -> None:
        """Deve preservar o caminho do PDF de origem."""
        text = "Processo nº 047799/2025-64"
        source_path = Path("/tmp/test.pdf")
        parser = Parser()
        result = parser.parse(text, source_pdf=source_path)
        
        assert result.source_pdf == source_path
        assert result.raw_text == text

    def test_parse_cpf_instead_of_cnpj(self) -> None:
        """Deve extrair CPF quando CNPJ não está presente."""
        text = (
            "Processo nº 047799/2025-64\n"
            "CPF 123.456.789-00"
        )
        parser = Parser()
        result = parser.parse(text)
        
        assert result.cpf_cnpj == "123.456.789-00"

    def test_parse_returns_processdata(self) -> None:
        """Deve sempre retornar uma instância de ProcessData."""
        parser = Parser()
        result = parser.parse("qualquer texto")
        
        assert isinstance(result, ProcessData)

    def test_parse_source_pdf_none(self) -> None:
        """Deve aceitar source_pdf como None."""
        text = "Processo nº 047799/2025-64"
        parser = Parser()
        result = parser.parse(text, source_pdf=None)
        
        assert result.source_pdf is None
        assert result.process_number == "047799/2025-64"

    def test_parse_preserves_raw_text(self) -> None:
        """Deve preservar exatamente o texto bruto fornecido."""
        text = (
            "Linha 1\n"
            "Linha 2\n"
            "Processo nº 047799/2025-64\n"
            "Linha 4"
        )
        parser = Parser()
        result = parser.parse(text)
        
        assert result.raw_text == text
