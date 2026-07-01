#!/usr/bin/env python3
"""
Orquestrador do workflow de processamento de PDFs.

Integra todos os componentes:
- PdfReader: lê texto bruto de PDFs
- Parser: extrai campos do texto
- ProcessData: contrato de dados
- WordGenerator: preenche template DOCX
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass

from src.pdf_reader import PdfReader, PdfReaderError
from src.parser import Parser, ParseError
from src.word_generator import WordGenerator, WordGeneratorError


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


@dataclass
class ProcessingResult:
    """
    Resultado do processamento de um PDF individual.
    
    Atributos:
        pdf_path: Caminho do PDF de origem
        success: Se o processamento foi bem-sucedido
        output_path: Caminho do DOCX gerado (se sucesso)
        error: Mensagem de erro (se falha)
    """
    pdf_path: Path
    success: bool
    output_path: Path | None = None
    error: str | None = None


class ProcessingEngine:
    """
    Orquestrador responsável por coordenar o processamento de PDFs.
    
    Integra leitura de PDF, parsing e geração de DOCX.
    """
    
    def __init__(self):
        """Inicializar engine com componentes."""
        self.pdf_reader = PdfReader()
        self.parser = Parser()
        self.word_generator = WordGenerator()
    
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
    
    def process_pdf(
        self,
        pdf_path: Path,
        template_path: Path,
        output_dir: Path,
    ) -> ProcessingResult:
        """
        Processar um PDF individual: ler, extrair, gerar DOCX.
        
        Args:
            pdf_path: Caminho do PDF a processar
            template_path: Caminho do template DOCX
            output_dir: Diretório para salvar DOCX gerado
            
        Returns:
            ProcessingResult com status e caminho do output
        """
        try:
            # 1. Ler PDF
            pdf_text = self.pdf_reader.read(pdf_path)
            
            # DIAGNOSTIC: Print raw PDF text (first 1000 chars)
            print("\n" + "="*50)
            print("===== RAW PDF TEXT =====")
            print(pdf_text[:1000])
            print("="*50)
            
            # 2. Parse dos dados
            process_data = self.parser.parse(pdf_text, source_pdf=pdf_path)
            
            # DIAGNOSTIC: Print extracted process data
            print("\n" + "="*50)
            print("===== PROCESS DATA =====")
            print(f"process_number: {process_data.process_number}")
            print(f"infraction_number: {process_data.infraction_number}")
            print(f"cpf_cnpj: {process_data.cpf_cnpj}")
            print("="*50 + "\n")
            
            # 3. Gerar DOCX
            output_filename = pdf_path.stem + ".docx"
            output_path = output_dir / output_filename
            
            self.word_generator.generate(
                template_path=template_path,
                process_data=process_data,
                output_path=output_path,
            )
            
            return ProcessingResult(
                pdf_path=pdf_path,
                success=True,
                output_path=output_path,
            )
        
        except PdfReaderError as e:
            return ProcessingResult(
                pdf_path=pdf_path,
                success=False,
                error=f"Erro ao ler PDF: {str(e)}",
            )
        except ParseError as e:
            return ProcessingResult(
                pdf_path=pdf_path,
                success=False,
                error=f"Erro ao fazer parse: {str(e)}",
            )
        except WordGeneratorError as e:
            return ProcessingResult(
                pdf_path=pdf_path,
                success=False,
                error=f"Erro ao gerar DOCX: {str(e)}",
            )
        except Exception as e:
            return ProcessingResult(
                pdf_path=pdf_path,
                success=False,
                error=f"Erro inesperado: {str(e)}",
            )
    
    def process_batch(
        self,
        input_dir: Path,
        template_path: Path,
        output_dir: Path,
    ) -> list[ProcessingResult]:
        """
        Processar batch de PDFs: ler pasta, processar cada PDF.
        
        Args:
            input_dir: Diretório com PDFs de entrada
            template_path: Caminho do template DOCX
            output_dir: Diretório para salvar DOCXs gerados
            
        Returns:
            Lista de ProcessingResult para cada PDF
            
        Raises:
            ValueError: Se pastas ou template não existirem
        """
        # Validar entradas
        input_path = Path(input_dir)
        template = Path(template_path)
        output_path = Path(output_dir)
        
        if not input_path.exists():
            raise ValueError(f"Pasta de entrada não encontrada: {input_path}")
        
        if not template.exists():
            raise ValueError(f"Template não encontrado: {template}")
        
        if not output_path.exists():
            raise ValueError(f"Pasta de saída não encontrada: {output_path}")
        
        # Escanear PDFs
        scan_result = self.scan_input_folder(input_path)
        
        # Processar cada PDF
        results = []
        for pdf_file in scan_result.pdf_files:
            result = self.process_pdf(pdf_file, template, output_path)
            results.append(result)
        
        return results
