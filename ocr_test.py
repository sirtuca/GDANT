#!/usr/bin/env python3
"""
OCR Test Script - Validate OCR quality on scanned PDFs.

Converts all pages of a PDF to images and extracts text using OCRReader.
Generates a validation report with complete extracted text for quality assessment.

Reuses the same OCR pipeline used by PdfReader.

Usage:
    python ocr_test.py <pdf_path>

Example:
    python ocr_test.py "C:\\Users\\Arthur\\Documents\\processo.pdf"

Output:
    Creates <pdf_name>_ocr_output.txt in the same directory as the PDF.
"""

import sys
import time
from pathlib import Path
from datetime import datetime

try:
    from pdf2image import convert_from_path
except ImportError:
    print("ERROR: pdf2image is not installed.")
    print("\nTo install, run:")
    print("  pip install pdf2image")
    print("\nYou also need Poppler installed on your system:")
    print("  Windows: choco install poppler")
    print("  macOS: brew install poppler")
    print("  Linux: sudo apt-get install poppler-utils")
    sys.exit(1)

from src.ocr_reader import OCRReader


def main():
    """
    Main function for OCR testing.
    """
    # Validate command line arguments
    if len(sys.argv) < 2:
        print("Usage: python ocr_test.py <pdf_path>")
        print("Example: python ocr_test.py 'processo.pdf'")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    
    # Validate PDF file exists
    if not pdf_path.exists():
        print(f"ERROR: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    if pdf_path.suffix.lower() != ".pdf":
        print(f"ERROR: File is not a PDF: {pdf_path}")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("[OCR_TEST] Starting OCR validation")
    print(f"[OCR_TEST] PDF: {pdf_path.name}")
    print("="*60 + "\n")
    
    execution_start = time.time()
    
    try:
        # Step 1: Convert all pages to images (ONLY ONCE)
        print("[OCR_TEST] Converting PDF to images (DPI=300)...")
        convert_start = time.time()
        images = convert_from_path(str(pdf_path), dpi=300)
        convert_time = time.time() - convert_start
        print(f"[OCR_TEST] ✓ Converted {len(images)} pages in {convert_time:.2f}s\n")
        
        # Step 2: Initialize OCRReader (lazy load)
        print("[OCR_TEST] Initializing OCRReader...")
        ocr_init_start = time.time()
        ocr_reader = OCRReader()
        
        # Step 3: Extract text using batch API (PaddleOCR initialized once)
        print(f"[OCR_TEST] Running OCR on {len(images)} pages...\n")
        batch_start = time.time()
        extracted_texts = ocr_reader.extract_batch(images)
        batch_time = time.time() - batch_start
        print(f"\n[OCR_TEST] ✓ OCR batch completed in {batch_time:.2f}s\n")
        
        # Step 4: Build output report
        output_lines = []
        total_characters = 0
        pages_with_text = 0
        pages_without_text = 0
        
        # Header: Validation Report
        output_lines.append("="*60)
        output_lines.append("OCR VALIDATION REPORT")
        output_lines.append("="*60)
        output_lines.append("")
        output_lines.append(f"PDF: {pdf_path.name}")
        output_lines.append(f"Total pages: {len(images)}")
        output_lines.append(f"DPI: 300")
        output_lines.append(f"OCR Engine: PaddleOCR")
        output_lines.append(f"Language: Portuguese")
        output_lines.append(f"Execution date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output_lines.append("")
        output_lines.append("="*60)
        output_lines.append("")
        output_lines.append("")
        
        # Process each extracted text
        for page_num, extracted_text in enumerate(extracted_texts, start=1):
            char_count = len(extracted_text)
            total_characters += char_count
            
            # Track pages with/without text
            if char_count > 0:
                pages_with_text += 1
            else:
                pages_without_text += 1
            
            # Warn if very little text extracted
            if 0 < char_count < 20:
                print(f"[OCR_TEST] WARNING: Page {page_num} has very little text ({char_count} chars)")
                print(f"  → Possible causes: poor scan quality, OCR issues, unsupported format")
            
            # Format page output
            output_lines.append("="*60)
            output_lines.append(f"PAGE {page_num}")
            output_lines.append("Source: OCR")
            output_lines.append(f"Characters: {char_count}")
            output_lines.append("="*60)
            output_lines.append("")
            
            if extracted_text:
                output_lines.append(extracted_text)
            else:
                output_lines.append("(No text extracted)")
            
            output_lines.append("")
            output_lines.append("")
        
        # Step 5: Save output file
        output_path = pdf_path.parent / f"{pdf_path.stem}_ocr_output.txt"
        
        print(f"[OCR_TEST] Saving output to {output_path.name}...", end=" ", flush=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        print("✓")
        
        # Step 6: Print summary
        total_time = time.time() - execution_start
        avg_chars_per_page = total_characters // len(images) if images else 0
        
        print("\n" + "-"*60)
        print("[OCR_TEST] OCR FINISHED")
        print("-"*60)
        print(f"Pages processed: {len(images)}")
        print(f"Pages with text: {pages_with_text}")
        print(f"Pages without text: {pages_without_text}")
        print(f"Characters extracted: {total_characters}")
        print(f"Average chars/page: {avg_chars_per_page}")
        print(f"Execution time: {total_time:.2f}s")
        print(f"Output file: {output_path}")
        print("-"*60 + "\n")
        
        return 0
    
    except ImportError as e:
        print(f"\n✗ ERROR: ImportError")
        print(f"  {e}")
        print(f"\nRequired packages:")
        print(f"  pip install pdf2image paddleocr")
        print(f"\nRequired system dependencies:")
        print(f"  Windows: choco install poppler")
        print(f"  macOS: brew install poppler")
        print(f"  Linux: sudo apt-get install poppler-utils")
        import traceback
        traceback.print_exc()
        return 1
    
    except Exception as e:
        print(f"\n✗ ERROR during OCR processing: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
