#!/usr/bin/env python3
"""
Leitor de texto de arquivos PDF usando PyMuPDF (fitz).

Este módulo extrai texto bruto de PDFs, preservando a ordem das páginas.
Não utiliza OCR, interpretação de texto ou extração de campos.
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass

import fitz


@dataclass
class PdfPageText:
    """
    Texto extraído de uma página de PDF.
    
    Atributos:
        page_number: Número da página (começando em 1)
        text: Texto extraído da página
    """
    page_number: int
    text: str


@dataclass
class PdfTextResult:
    """
    Resultado da leitura de texto de um PDF.
    
    Atributos:
        file_path: Caminho do arquivo PDF lido
        pages: Lista de páginas com texto extraído
        full_text: Texto completo do PDF (concatenado)
    """
    file_path: Path
    pages: list[PdfPageText]
    full_text: str


class PdfReader:
    """
    Leitor de texto de arquivos PDF.
    
    Extrai o texto bruto de cada página, preservando a ordem.
    """
    
    def read_text(self, pdf_path: Path) -> PdfTextResult:
        """
        Extrair texto de um arquivo PDF.
        
        Args:
            pdf_path: Caminho do arquivo PDF
        
        Returns:
            PdfTextResult contendo texto de todas as páginas
            
        Raises:
            FileNotFoundError: Se o arquivo não existe
            ValueError: Se o caminho não é um arquivo PDF ou não pode ser aberto
        """
        pdf_file = Path(pdf_path)
        
        # Validar existência
        if not pdf_file.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {pdf_file}")
        
        # Validar extensão
        if pdf_file.suffix.lower() != ".pdf":
            raise ValueError(f"Arquivo não é um PDF: {pdf_file}")
        
        try:
            # Abrir PDF
            doc = fitz.open(pdf_file)
        except fitz.FileError as e:
            raise ValueError(f"Não foi possível abrir o PDF: {pdf_file}") from e
        except Exception as e:
            raise ValueError(f"Erro ao processar PDF: {pdf_file}") from e
        
        # Extrair texto de cada página
        pages = []
        full_text_parts = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            
            pages.append(PdfPageText(
                page_number=page_num + 1,
                text=page_text
            ))
            
            full_text_parts.append(page_text)
        
        # Fechar documento
        doc.close()
        
        # Concatenar todo o texto com quebra entre páginas
        full_text = "\n\n".join(full_text_parts)
        
        return PdfTextResult(
            file_path=pdf_file,
            pages=pages,
            full_text=full_text
        )
