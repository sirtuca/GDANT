#!/usr/bin/env python3
"""
Testes para o módulo pdf_reader.

Valida leitura de PDFs e extração de texto.
"""

from __future__ import annotations

from pathlib import Path
from io import BytesIO

import pytest
import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from src.pdf_reader import PdfReader, PdfReaderError


@pytest.fixture
def temp_dir(tmp_path):
    """Diretório temporário para testes."""
    return tmp_path


@pytest.fixture
def sample_pdf(temp_dir):
    """Cria um PDF simples com texto para teste."""
    pdf_path = temp_dir / "sample.pdf"
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Processo nº 047799/2025-64")
    c.drawString(100, 730, "Auto de Infração 30697/25")
    c.showPage()
    c.save()
    
    with open(pdf_path, "wb") as f:
        f.write(buffer.getvalue())
    
    return pdf_path


@pytest.fixture
def multipage_pdf(temp_dir):
    """Cria um PDF com múltiplas páginas."""
    pdf_path = temp_dir / "multipage.pdf"
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Página 1
    c.drawString(100, 750, "Página 1: Primeiro texto")
    c.showPage()
    
    # Página 2
    c.drawString(100, 750, "Página 2: Segundo texto")
    c.showPage()
    
    # Página 3
    c.drawString(100, 750, "Página 3: Terceiro texto")
    c.showPage()
    
    c.save()
    
    with open(pdf_path, "wb") as f:
        f.write(buffer.getvalue())
    
    return pdf_path


@pytest.fixture
def empty_pdf(temp_dir):
    """Cria um PDF vazio."""
    pdf_path = temp_dir / "empty.pdf"
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.showPage()
    c.save()
    
    with open(pdf_path, "wb") as f:
        f.write(buffer.getvalue())
    
    return pdf_path


class TestPdfReader:
    """Testes para a classe PdfReader."""

    def test_read_existing_pdf(self, sample_pdf):
        """Deve ler PDF existente com sucesso."""
        reader = PdfReader()
        text = reader.read(sample_pdf)
        
        assert isinstance(text, str)
        assert "Processo nº 047799/2025-64" in text
        assert "Auto de Infração 30697/25" in text

    def test_read_invalid_path(self):
        """Deve lançar erro para caminho inválido."""
        reader = PdfReader()
        invalid_path = Path("/tmp/nao_existe_12345.pdf")
        
        with pytest.raises(PdfReaderError):
            reader.read(invalid_path)

    def test_read_empty_pdf(self, empty_pdf):
        """Deve ler PDF vazio sem erro."""
        reader = PdfReader()
        text = reader.read(empty_pdf)
        
        assert isinstance(text, str)
        assert text == ""

    def test_read_multipage_pdf(self, multipage_pdf):
        """Deve ler PDF com múltiplas páginas."""
        reader = PdfReader()
        text = reader.read(multipage_pdf)
        
        assert "Página 1" in text
        assert "Página 2" in text
        assert "Página 3" in text
        # Páginas separadas por "\n\n"
        assert "\n\n" in text

    def test_read_returns_string(self, sample_pdf):
        """Deve retornar sempre string."""
        reader = PdfReader()
        text = reader.read(sample_pdf)
        
        assert isinstance(text, str)

    def test_read_preserves_order(self, multipage_pdf):
        """Deve preservar ordem de páginas."""
        reader = PdfReader()
        text = reader.read(multipage_pdf)
        
        # Verificar que Página 1 vem antes de Página 2
        idx_page1 = text.find("Página 1")
        idx_page2 = text.find("Página 2")
        idx_page3 = text.find("Página 3")
        
        assert idx_page1 < idx_page2 < idx_page3
