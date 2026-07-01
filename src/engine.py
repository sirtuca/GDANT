#!/usr/bin/env python3
"""
Orquestrador do workflow de processamento de PDFs - Sprint 2.

Sprint 2 Objetivo:
- Escanear a pasta de entrada
- Encontrar arquivos PDF
- Retornar lista de PDFs ordenada
- Sem processamento de arquivos

Responsabilidades:
- Validar existência e tipo da pasta
- Listar arquivos .pdf
- Ordenar resultados
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass


@dataclass
class PdfScanResult:
    """
    Resultado da varredura de PDFs em uma pasta.
    
    Atributos:
        folder: Caminho da pasta escaneada
        pdf_files: Lista de caminhos para arquivos PDF encontrados
        total: Quantidade total de PDFs encontrados
    """
    folder: Path
    pdf_files: list[Path]
    total: int


class ProcessingEngine:
    """
    Orquestrador responsável por coordenar o processamento de PDFs.
    
    Na Sprint 2, responsável apenas por escanear a pasta de entrada
    e retornar lista de PDFs.
    """
    
    def scan_input_folder(self, input_dir: Path) -> PdfScanResult:
        """
        Escanear pasta de entrada e retornar PDFs encontrados.
        
        Args:
            input_dir: Caminho da pasta a escanear
        
        Returns:
            PdfScanResult com lista de PDFs ordenada
            
        Raises:
            ValueError: Se a pasta não existir ou não for diretório
        """
        folder_path = Path(input_dir)
        
        # Validar existência
        if not folder_path.exists():
            raise ValueError(f"Pasta não encontrada: {folder_path}")
        
        # Validar que é diretório
        if not folder_path.is_dir():
            raise ValueError(f"Caminho não é um diretório: {folder_path}")
        
        # Buscar arquivos PDF (sem subpastas)
        pdf_files = sorted(folder_path.glob("*.pdf"))
        
        return PdfScanResult(
            folder=folder_path,
            pdf_files=pdf_files,
            total=len(pdf_files),
        )
