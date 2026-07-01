#!/usr/bin/env python3
"""
Leitor de PDFs para extração de texto bruto.

Este módulo extrai texto de PDFs mantendo ordem de páginas.
"""

from __future__ import annotations

from pathlib import Path

import pdfplumber


class PdfReaderError(Exception):
    """Erro ao ler PDF."""

    pass


class PdfReader:
    """
    Leitor de PDFs que extrai texto bruto.
    
    Retorna texto preservando ordem de páginas, separadas por "\n\n".
    """

    def read(self, pdf_path: Path) -> str:
        """
        Extrai texto completo de um PDF.
        
        Lê todas as páginas em ordem e retorna texto bruto.
        Páginas são separadas por "\n\n".
        
        Args:
            pdf_path: Caminho do arquivo PDF
            
        Returns:
            Texto completo do PDF
            
        Raises:
            PdfReaderError: Se arquivo não existir ou não puder ser lido
        """
        if not pdf_path.exists():
            raise PdfReaderError(f"Arquivo PDF não encontrado: {pdf_path}")

        try:
            with pdfplumber.open(str(pdf_path)) as pdf:
                pages_text = []
                
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pages_text.append(text)
                
                return "\n\n".join(pages_text)
                
        except Exception as e:
            raise PdfReaderError(f"Erro ao ler PDF: {e}") from e
