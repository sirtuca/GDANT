#!/usr/bin/env python3
"""
Leitor de PDFs para extração de texto bruto com suporte a OCR.

Este módulo extrai texto de PDFs mantendo ordem de páginas.
Suporta PDFs digitais, scaneados e mistos através de OCR automático.

Fluxo:
1. Para cada página, tenta pdfplumber.extract_text()
2. Se texto é insuficiente (< OCR_MIN_TEXT_LENGTH caracteres úteis), executa OCR
3. Mescla texto preservando ordem de páginas
4. Parser não sabe origem do texto (pdfplumber vs OCR)
"""

from __future__ import annotations

from pathlib import Path

import pdfplumber

from src.config import OCR_MIN_TEXT_LENGTH
from src.ocr_reader import OCRReader


class PdfReaderError(Exception):
    """Erro ao ler PDF."""

    pass


class PdfReader:
    """
    Leitor de PDFs que extrai texto bruto com suporte a OCR automático.
    
    Retorna texto preservando ordem de páginas, separadas por "\n\n".
    
    Workflow:
    - Tenta pdfplumber.extract_text() primeiro
    - Se texto < OCR_MIN_TEXT_LENGTH, executa OCR na página
    - Fallback: se OCR falhar, usa texto de pdfplumber (nunca interrompe)
    - Preserva ordem original das páginas
    
    OCRReader é inicializado apenas quando a primeira página realmente precisa de OCR.
    Se o PDF é completamente digital, OCRReader nunca é instanciado.
    """

    def __init__(self):
        """
        Inicializar PdfReader.
        
        OCRReader é inicializado de forma lazy (somente quando necessário).
        """
        self.ocr_reader = None  # Lazy initialization

    def read(self, pdf_path: Path) -> str:
        """
        Extrai texto completo de um PDF com OCR automático.
        
        Lê todas as páginas em ordem:
        1. Tenta pdfplumber.extract_text()
        2. Se texto insuficiente, executa OCR (inicializa OCRReader se necessário)
        3. Fallback: se OCR falhar, usa texto de pdfplumber
        4. Retorna texto consolidado preservando ordem
        
        Args:
            pdf_path: Caminho do arquivo PDF
            
        Returns:
            Texto completo do PDF (páginas separadas por "\n\n")
            
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
                print(f"[PDFREADER] OCR_MIN_TEXT_LENGTH: {OCR_MIN_TEXT_LENGTH}")
                print("="*80 + "\n")
                
                # DIAGNOSTIC: Create diagnostic output file
                diagnostic_output = []
                diagnostic_output.append(f"DIAGNÓSTICO DE EXTRAÇÃO PDF - {pdf_path.name}\n")
                diagnostic_output.append(f"Total de páginas: {len(pdf.pages)}\n")
                diagnostic_output.append(f"OCR_MIN_TEXT_LENGTH: {OCR_MIN_TEXT_LENGTH}\n")
                diagnostic_output.append("="*80 + "\n\n")
                
                pdfplumber_pages_count = 0
                ocr_attempts = 0
                ocr_successes = 0
                
                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extrair com pdfplumber
                    text_pdfplumber = page.extract_text()
                    
                    # Lazy: inicializar OCRReader apenas quando necessário
                    if self.ocr_reader is None and text_pdfplumber is not None:
                        # Verificar se vai precisar OCR
                        test_ocr_need = len(text_pdfplumber.strip()) < OCR_MIN_TEXT_LENGTH
                        if test_ocr_need or text_pdfplumber is None:
                            # Inicializar OCRReader agora
                            self.ocr_reader = OCRReader()
                    
                    # Decidir se precisa OCR
                    if self.ocr_reader is not None:
                        needs_ocr = self.ocr_reader.should_run_ocr(text_pdfplumber)
                    else:
                        # OCRReader não foi instanciado, então não precisa OCR
                        needs_ocr = False
                    
                    if not needs_ocr:
                        # Usar texto de pdfplumber
                        final_text = text_pdfplumber
                        extraction_method = "pdfplumber"
                        pdfplumber_pages_count += 1
                    else:
                        # Executar OCR
                        ocr_attempts += 1
                        extraction_method = "OCR tentativa"
                        
                        text_ocr = self.ocr_reader.extract_from_pdf_page(pdf_path, page_num - 1)
                        
                        if text_ocr:
                            # OCR bem-sucedido
                            final_text = text_ocr
                            extraction_method = "OCR (sucesso)"
                            ocr_successes += 1
                        else:
                            # OCR falhou, usar pdfplumber como fallback
                            final_text = text_pdfplumber if text_pdfplumber else ""
                            extraction_method = "OCR (falhou) → pdfplumber fallback"
                    
                    # DIAGNOSTIC: Print page statistics
                    char_count = len(final_text) if final_text else 0
                    print(f"[PDFREADER] Página {page_num:2d}: {char_count:5d} caracteres ({extraction_method})")
                    
                    if final_text:
                        first_300 = final_text[:300].replace("\n", " ")
                        last_300 = final_text[-300:].replace("\n", " ")
                        print(f"  Primeiros 300: {first_300}...")
                        print(f"  Últimos 300:   ...{last_300}\n")
                        pages_text.append(final_text)
                    else:
                        print(f"  (Página vazia após processamento)\n")
                        pages_text.append("")
                    
                    # DIAGNOSTIC: Add to diagnostic file
                    diagnostic_output.append(f"===== PÁGINA {page_num} =====")
                    diagnostic_output.append(f"\nMétodo de extração: {extraction_method}\n")
                    diagnostic_output.append(f"Caracteres extraídos: {char_count}\n\n")
                    diagnostic_output.append(f"===== CONTEÚDO PÁGINA {page_num} =====\n")
                    diagnostic_output.append(final_text if final_text else "[VAZIO]\n")
                    diagnostic_output.append("\n\n")
                
                # DIAGNOSTIC: Write diagnostic file
                diagnostic_path = pdf_path.parent / f"{pdf_path.stem}_diagnostic.txt"
                with open(diagnostic_path, "w", encoding="utf-8") as f:
                    f.writelines(diagnostic_output)
                
                print("="*80)
                print("[PDFREADER] Resumo de extração:")
                print(f"[PDFREADER]   - Total de páginas: {len(pdf.pages)}")
                print(f"[PDFREADER]   - Processadas com pdfplumber: {pdfplumber_pages_count}")
                print(f"[PDFREADER]   - OCR tentadas: {ocr_attempts}")
                print(f"[PDFREADER]   - OCR bem-sucedidas: {ocr_successes}")
                print(f"[PDFREADER]   - Total de caracteres extraídos: {sum(len(t) for t in pages_text)}")
                print(f"[PDFREADER]   - Arquivo diagnóstico: {diagnostic_path}")
                print("="*80 + "\n")
                
                return "\n\n".join(pages_text)
                
        except Exception as e:
            raise PdfReaderError(f"Erro ao ler PDF: {e}") from e
