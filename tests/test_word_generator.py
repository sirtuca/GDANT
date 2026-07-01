#!/usr/bin/env python3
"""
Testes para o WordGenerator.

Valida suporte a ambos os formatos de placeholders:
- Colchetes: [PROC], [AI], [DOC]
- Chevrons: <<PROC>>, <<AI>>, <<DOC>>
"""

import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.word_generator import WordGenerator, WordGeneratorError
from src.models import ProcessData


class TestWordGeneratorPlaceholders(unittest.TestCase):
    """Testes para substituição de placeholders no WordGenerator."""

    def setUp(self):
        """Configurar testes."""
        self.generator = WordGenerator()
        
        # Dados de teste
        self.process_data = ProcessData(
            process_number="047799/2025-64",
            infraction_number="30697/25",
            cpf_cnpj="12.345.678/0001-95",
        )

    def test_placeholder_map_contains_all_fields(self):
        """Verificar que PLACEHOLDER_MAP contém todos os campos necessários."""
        self.assertIn("PROC", self.generator.PLACEHOLDER_MAP)
        self.assertIn("AI", self.generator.PLACEHOLDER_MAP)
        self.assertIn("DOC", self.generator.PLACEHOLDER_MAP)
        
        self.assertEqual(self.generator.PLACEHOLDER_MAP["PROC"], "process_number")
        self.assertEqual(self.generator.PLACEHOLDER_MAP["AI"], "infraction_number")
        self.assertEqual(self.generator.PLACEHOLDER_MAP["DOC"], "cpf_cnpj")

    def test_replace_bracket_placeholders(self):
        """Testar substituição de placeholders com colchetes [PLACEHOLDER]."""
        # Mock do parágrafo
        mock_run = Mock()
        mock_run.text = "Processo: [PROC], Infração: [AI], CPF: [DOC]"
        
        mock_paragraph = Mock()
        mock_paragraph.runs = [mock_run]
        
        # Substituir placeholders
        self.generator._replace_placeholders_in_paragraph(
            mock_paragraph, self.process_data
        )
        
        # Verificar substituições
        expected = "Processo: 047799/2025-64, Infração: 30697/25, CPF: 12.345.678/0001-95"
        self.assertEqual(mock_run.text, expected)

    def test_replace_chevron_placeholders(self):
        """Testar substituição de placeholders com chevrons <<PLACEHOLDER>>."""
        # Mock do parágrafo
        mock_run = Mock()
        mock_run.text = "Processo: <<PROC>>, Infração: <<AI>>, CPF: <<DOC>>"
        
        mock_paragraph = Mock()
        mock_paragraph.runs = [mock_run]
        
        # Substituir placeholders
        self.generator._replace_placeholders_in_paragraph(
            mock_paragraph, self.process_data
        )
        
        # Verificar substituições
        expected = "Processo: 047799/2025-64, Infração: 30697/25, CPF: 12.345.678/0001-95"
        self.assertEqual(mock_run.text, expected)

    def test_replace_mixed_placeholders(self):
        """Testar substituição com mistura de formatos [PLACEHOLDER] e <<PLACEHOLDER>>."""
        # Mock do parágrafo
        mock_run = Mock()
        mock_run.text = "Processo: [PROC], Infração: <<AI>>, CPF: [DOC]"
        
        mock_paragraph = Mock()
        mock_paragraph.runs = [mock_run]
        
        # Substituir placeholders
        self.generator._replace_placeholders_in_paragraph(
            mock_paragraph, self.process_data
        )
        
        # Verificar substituições
        expected = "Processo: 047799/2025-64, Infração: 30697/25, CPF: 12.345.678/0001-95"
        self.assertEqual(mock_run.text, expected)

    def test_no_replacement_for_unknown_placeholders(self):
        """Testar que placeholders desconhecidos não são substituídos."""
        # Mock do parágrafo
        mock_run = Mock()
        mock_run.text = "Texto com [UNKNOWN] e <<NOTFOUND>>"
        
        mock_paragraph = Mock()
        mock_paragraph.runs = [mock_run]
        
        # Substituir placeholders
        self.generator._replace_placeholders_in_paragraph(
            mock_paragraph, self.process_data
        )
        
        # Verificar que texto não foi alterado
        self.assertEqual(mock_run.text, "Texto com [UNKNOWN] e <<NOTFOUND>>")

    def test_empty_data_values(self):
        """Testar substituição com dados vazios."""
        empty_data = ProcessData(
            process_number="",
            infraction_number="",
            cpf_cnpj="",
        )
        
        # Mock do parágrafo
        mock_run = Mock()
        mock_run.text = "Processo: [PROC], Infração: [AI], CPF: [DOC]"
        
        mock_paragraph = Mock()
        mock_paragraph.runs = [mock_run]
        
        # Substituir placeholders
        self.generator._replace_placeholders_in_paragraph(
            mock_paragraph, empty_data
        )
        
        # Verificar que placeholders foram substituídos por strings vazias
        expected = "Processo: , Infração: , CPF: "
        self.assertEqual(mock_run.text, expected)

    def test_multiple_runs_with_placeholders(self):
        """Testar parágrafo com múltiplos runs contendo placeholders."""
        # Múltiplos runs
        mock_run1 = Mock()
        mock_run1.text = "Processo: [PROC]"
        
        mock_run2 = Mock()
        mock_run2.text = "Infração: <<AI>>"
        
        mock_paragraph = Mock()
        mock_paragraph.runs = [mock_run1, mock_run2]
        
        # Substituir placeholders
        self.generator._replace_placeholders_in_paragraph(
            mock_paragraph, self.process_data
        )
        
        # Verificar substituições em cada run
        self.assertEqual(mock_run1.text, "Processo: 047799/2025-64")
        self.assertEqual(mock_run2.text, "Infração: 30697/25")

    def test_placeholder_not_found_in_run(self):
        """Testar run que não contém nenhum placeholder."""
        # Mock do parágrafo
        mock_run = Mock()
        mock_run.text = "Texto normal sem placeholders"
        
        mock_paragraph = Mock()
        mock_paragraph.runs = [mock_run]
        
        original_text = mock_run.text
        
        # Substituir placeholders
        self.generator._replace_placeholders_in_paragraph(
            mock_paragraph, self.process_data
        )
        
        # Verificar que texto não foi alterado
        self.assertEqual(mock_run.text, original_text)

    def test_template_not_found_error(self):
        """Testar erro quando template não existe."""
        non_existent_path = Path("/tmp/non_existent_template_12345.docx")
        
        with self.assertRaises(WordGeneratorError) as context:
            self.generator.generate(
                template_path=non_existent_path,
                process_data=self.process_data,
                output_path=Path("/tmp/output.docx"),
            )
        
        self.assertIn("Template não encontrado", str(context.exception))

    def test_partial_placeholder_not_replaced(self):
        """Testar que placeholders parciais não são substituídos."""
        # Mock do parágrafo
        mock_run = Mock()
        mock_run.text = "Texto com [PROC (incompleto) e <<AI (incompleto)"
        
        mock_paragraph = Mock()
        mock_paragraph.runs = [mock_run]
        
        original_text = mock_run.text
        
        # Substituir placeholders
        self.generator._replace_placeholders_in_paragraph(
            mock_paragraph, self.process_data
        )
        
        # Verificar que texto não foi alterado (placeholders incompletos)
        self.assertEqual(mock_run.text, original_text)


if __name__ == "__main__":
    unittest.main()
