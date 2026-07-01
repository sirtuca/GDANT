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
                
                # DIAGNOSTIC: Print PDF info
                print("\n" + "="*80)
                print("[PDFREADER] Iniciando extração de PDF")
                print(f"[PDFREADER] Caminho: {pdf_path}")
                print(f"[PDFREADER] Total de páginas no PDF: {len(pdf.pages)}")
                print("="*80 + "\n")
                
                # DIAGNOSTIC: Create diagnostic output file
                diagnostic_output = []
                diagnostic_output.append(f"DIAGNÓSTICO DE EXTRAÇÃO PDF - {pdf_path.name}\n")
                diagnostic_output.append(f"Total de páginas: {len(pdf.pages)}\n")
                diagnostic_output.append("="*80 + "\n\n")
                
                for page_num, page in enumerate(pdf.pages, start=1):
                    # DIAGNOSTIC: Extract with both modes
                    text_default = page.extract_text()
                    text_layout = page.extract_text(layout=True)
                    
                    char_default = len(text_default) if text_default else 0
                    char_layout = len(text_layout) if text_layout else 0
                    
                    # DIAGNOSTIC: Print page comparison
                    print(f"[PDFREADER] Página {page_num:2d}:")
                    print(f"  DEFAULT mode: {char_default:5d} caracteres")
                    print(f"  LAYOUT mode:  {char_layout:5d} caracteres")
                    
                    # Use default mode for actual processing
                    if text_default:
                        pages_text.append(text_default)
                        first_300 = text_default[:300].replace("\n", " ")
                        last_300 = text_default[-300:].replace("\n", " ")
                        print(f"  Primeiros 300: {first_300}...")
                        print(f"  Últimos 300:   ...{last_300}\n")
                    else:
                        print(f"  NENHUM TEXTO EXTRAÍDO (None ou vazio)\n")
                    
                    # DIAGNOSTIC: Add to diagnostic file
                    diagnostic_output.append(f"===== PÁGINA {page_num} =====\n")
                    diagnostic_output.append(f"DEFAULT mode: {char_default} caracteres\n")
                    diagnostic_output.append(f"LAYOUT mode:  {char_layout} caracteres\n\n")
                    
                    # If modes differ, save both versions
                    if text_default != text_layout:
                        diagnostic_output.append(f"===== PÁGINA {page_num} - DEFAULT =====\n")
                        diagnostic_output.append(text_default if text_default else "[VAZIO]\n")
                        diagnostic_output.append("\n\n")
                        
                        diagnostic_output.append(f"===== PÁGINA {page_num} - LAYOUT =====\n")
                        diagnostic_output.append(text_layout if text_layout else "[VAZIO]\n")
                        diagnostic_output.append("\n\n")
                    else:
                        # If same, save once
                        diagnostic_output.append(f"===== PÁGINA {page_num} - CONTEÚDO =====\n")
                        diagnostic_output.append(text_default if text_default else "[VAZIO]\n")
                        diagnostic_output.append("\n\n")
                
                # DIAGNOSTIC: Write diagnostic file
                diagnostic_path = pdf_path.parent / f"{pdf_path.stem}_diagnostic.txt"
                with open(diagnostic_path, "w", encoding="utf-8") as f:
                    f.writelines(diagnostic_output)
                
                print("="*80)
                print(f"[PDFREADER] Total de páginas processadas: {len(pages_text)}/{len(pdf.pages)}")
                print(f"[PDFREADER] Arquivo diagnóstico salvo em: {diagnostic_path}")
                print("="*80 + "\n")
                
                return "\n\n".join(pages_text)
                
        except Exception as e:
            raise PdfReaderError(f"Erro ao ler PDF: {e}") from e
