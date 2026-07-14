#!/usr/bin/env python3
"""
Leitor OCR para páginas de PDF com pouco ou nenhum texto vetorial.

Este módulo extrai texto de páginas scaneadas usando PaddleOCR.
Isolado do Parser e Extractors.

Workflow:
1. PdfReader tenta pdfplumber.extract_text()
2. Se texto < OCR_MIN_TEXT_LENGTH caracteres úteis, OCRReader processa a página
3. Texto final é mesclado preservando ordem de páginas
4. Parser não sabe origem do texto

Dependências externas:
- paddleocr: pip install paddleocr
- pdf2image: pip install pdf2image
- poppler-utils (Windows): ver SETUP.md para instruções

Para detalhes de instalação, consulte SETUP.md
"""

from __future__ import annotations

import traceback
from pathlib import Path
from typing import Optional

from PIL.Image import Image

from src.config import OCR_MIN_TEXT_LENGTH, OCR_DPI


class OCRReaderError(Exception):
    """Erro ao processar OCR."""
    pass


class OCRReader:
    """
    Leitor OCR para páginas scaneadas de PDF.
    
    Usa PaddleOCR para extrair texto de imagens de páginas.
    Suporta português como idioma padrão.
    
    Lazy initialization: PaddleOCR é carregado apenas na primeira página OCR.
    """
    
    # Lazy initialization: classe variável para compartilhar instância
    _ocr_instance: Optional[object] = None
    
    def __init__(self, ocr_min_text_length: Optional[int] = None):
        """
        Inicializar OCRReader.
        
        Args:
            ocr_min_text_length: Mínimo de caracteres úteis para considerar 
                               texto de pdfplumber suficiente. Se None, usa
                               valor padrão de OCR_MIN_TEXT_LENGTH.
        """
        self.ocr_min_text_length = ocr_min_text_length or OCR_MIN_TEXT_LENGTH
    
    @classmethod
    def _initialize_ocr(cls) -> object:
        """
        Lazy initialization de PaddleOCR.
        
        Carrega o modelo apenas na primeira execução.
        Compartilha instância entre múltiplas chamadas.
        
        Returns:
            Instância de PaddleOCR
            
        Raises:
            OCRReaderError: Se PaddleOCR não puder ser inicializado
        """
        if cls._ocr_instance is not None:
            return cls._ocr_instance
        
        try:
            from paddleocr import PaddleOCR
            
            # Inicializar com suporte a português (v3.7.0+)
            # use_angle_cls=True: corrige rotação de texto
            # lang='pt': suporte a português (string, não lista)
            # use_gpu=False: usar CPU (mais compatível)
            print("[OCREADER] Inicializando PaddleOCR com suporte a português...")
            cls._ocr_instance = PaddleOCR(
                use_angle_cls=True,
                lang='pt',
                use_gpu=False
            )
            print("[OCREADER] PaddleOCR inicializado com sucesso (lazy)")
            return cls._ocr_instance
            
        except ImportError as e:
            print("[OCREADER] ERRO: ImportError ao carregar PaddleOCR")
            traceback.print_exc()
            raise OCRReaderError(
                f"PaddleOCR não está instalado. Instale com: pip install paddleocr\n"
                f"Para detalhes completos, consulte SETUP.md"
            ) from e
        except Exception as e:
            print("[OCREADER] ERRO: Exceção ao inicializar PaddleOCR")
            traceback.print_exc()
            raise OCRReaderError(f"Erro ao inicializar PaddleOCR: {e}") from e
    
    def extract_from_page_image(self, pil_image: Image) -> str:
        """
        Extrai texto de uma imagem de página usando OCR.
        
        Args:
            pil_image: PIL Image object da página
            
        Returns:
            Texto extraído via OCR, ou string vazia se falhar
        """
        try:
            ocr = self._initialize_ocr()
            
            # Executar OCR na imagem
            # result é: [[text, confidence], [...], ...] por linha detectada
            result = ocr.ocr(pil_image, cls=True)
            
            if result and result[0]:
                extracted_lines = []
                for line in result[0]:
                    if line and len(line) >= 2:
                        # line[1] é tupla (text, confidence)
                        text_box = line[1]
                        if text_box and isinstance(text_box, tuple) and len(text_box) >= 1:
                            text = text_box[0]
                            if text:
                                extracted_lines.append(text)
                
                return "\n".join(extracted_lines)
            
            return ""
        except Exception as e:
            print(f"[OCREADER] ERRO ao processar OCR da página:")
            traceback.print_exc()
            return ""
    
    def extract_batch(self, images: list[Image]) -> list[str]:
        """
        Extrai texto de múltiplas imagens de páginas usando OCR.
        
        Processa todas as imagens mantendo ordem.
        Inicializa PaddleOCR uma única vez antes do lote.
        Se uma página falhar, retorna string vazia e continua com as próximas.
        
        Args:
            images: Lista de PIL Image objects
            
        Returns:
            Lista de textos extraídos (um por imagem)
        """
        extracted_texts = []
        
        # Inicializar PaddleOCR uma única vez
        try:
            ocr = self._initialize_ocr()
        except OCRReaderError:
            # Se inicialização falhar, retornar lista de strings vazias
            return [""] * len(images)
        
        # Processar cada imagem
        for image in images:
            try:
                # Executar OCR na imagem
                result = ocr.ocr(image, cls=True)
                
                if result and result[0]:
                    extracted_lines = []
                    for line in result[0]:
                        if line and len(line) >= 2:
                            text_box = line[1]
                            if text_box and isinstance(text_box, tuple) and len(text_box) >= 1:
                                text = text_box[0]
                                if text:
                                    extracted_lines.append(text)
                    
                    extracted_texts.append("\n".join(extracted_lines))
                else:
                    extracted_texts.append("")
            
            except Exception as e:
                print(f"[OCREADER] ERRO ao processar página do lote:")
                traceback.print_exc()
                extracted_texts.append("")
        
        return extracted_texts
    
    def should_run_ocr(self, text: str) -> bool:
        """
        Determina se uma página precisa de OCR.
        
        Critério: se texto útil < self.ocr_min_text_length caracteres, OCR é necessário.
        Texto útil = texto após remover espaços em branco.
        
        Args:
            text: Texto extraído por pdfplumber
            
        Returns:
            True se OCR deve ser executado, False caso contrário
        """
        if not text:
            return True
        
        useful_text = text.strip()
        return len(useful_text) < self.ocr_min_text_length
