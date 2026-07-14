# Guia do Parser - GDANT

## Responsabilidade do Parser

O Parser é responsável por:

1. **Coordenar Extractors** - Disparar extractors especializados
2. **Assemblar ProcessData** - Consolidar dados em estrutura única
3. **Validar Coerência** - Garantir consistência entre campos
4. **Retornar Contrato** - Devolver ProcessData preenchido

## Fluxo do Parser

```
Texto Bruto (raw_text)
    ↓
[Parser]
    ├→ ExtractorProcessNumber → process_number
    ├→ ExtractorCpf → cpf_cnpj
    ├→ ExtractorCnpj → cpf_cnpj (se CPF não encontrado)
    ├→ ExtractorEmail → email
    ├→ ExtractorPhone → phone
    ├→ ExtractorTaxpayerName → taxpayer_name
    ├→ ExtractorAddress → address
    ├→ ExtractorCity → city
    ├→ ExtractorState → state
    ├→ ExtractorZipCode → zip_code
    ├→ ExtractorInfractionNumber → infraction_number
    ├→ ExtractorNotificationDate → notification_date
    ├→ ExtractorJudgmentDate → judgment_date
    ├→ ExtractorJudgmentNotificationDate → judgment_notification_date
    ├→ ExtractorArNumber → ar_number
    ├→ ExtractorDebtAmount → debt_amount
    ├→ ExtractorLegalBasis → legal_basis[]
    └→ ExtractorObservations → observations[]
    ↓
ProcessData (Consolidado)
```

## Estrutura do Parser

```python
from models import ProcessData
from extractors import (
    ExtractorProcessNumber,
    ExtractorCpf,
    ExtractorCnpj,
    # ... outros extractors
)
from decimal import Decimal
from pathlib import Path

class Parser:
    """Parser que assembla ProcessData a partir de texto bruto."""
    
    def __init__(self):
        """Inicializa parser com extractors."""
        self.extractor_process_number = ExtractorProcessNumber()
        self.extractor_cpf = ExtractorCpf()
        # ... inicializar outros extractors
    
    def parse(self, text: str, source_pdf: Path | None = None) -> ProcessData:
        """
        Parse texto bruto e retorna ProcessData.
        
        Args:
            text: Texto bruto extraído do PDF
            source_pdf: Caminho do PDF de origem (opcional)
        
        Returns:
            ProcessData preenchido com dados extraídos
        """
        # Extrair dados
        process_number = self.extractor_process_number.extract(text)
        cpf_cnpj = self.extractor_cpf.extract(text) or self.extractor_cnpj.extract(text)
        email = self.extractor_email.extract(text)
        # ... extrair outros dados
        
        # Validar coerência
        self._validate_coherence({
            "process_number": process_number,
            "cpf_cnpj": cpf_cnpj,
            # ... outros dados
        })
        
        # Assemblar ProcessData
        process_data = ProcessData(
            source_pdf=source_pdf,
            raw_text=text,
            process_number=process_number or "",
            cpf_cnpj=cpf_cnpj or "",
            email=email or "",
            # ... outros campos
        )
        
        return process_data
    
    def _validate_coherence(self, data: dict) -> None:
        """Valida coerência entre campos."""
        # Implementar validações
        pass
```

## Validações do Parser

### Validações Básicas

1. **Nenhum campo obrigatório nulo**
   - Pelo menos process_number deve estar presente

2. **Coerência de Documentos**
   - CPF ou CNPJ deve estar presente
   - Se CPF, deve ter 11 dígitos
   - Se CNPJ, deve ter 14 dígitos

3. **Coerência de Datas**
   - notification_date ≤ judgment_date ≤ judgment_notification_date

4. **Coerência de Valores**
   - debt_amount ≥ 0

5. **Listas Não Vazias**
   - legal_basis não deve estar vazio (pelo menos uma)

## Tratamento de Erros

```python
class ParseError(Exception):
    """Erro durante parsing."""
    pass

class Parser:
    def parse(self, text: str) -> ProcessData:
        try:
            # ... extração de dados
            if not process_number:
                raise ParseError("Número do processo não encontrado")
            
            # ... validações
        
        except ParseError as e:
            # Log erro
            raise
```

## Estratégia de Extração

### Estratégia 1: Todas as Informações (Padrão)

```python
def parse(self, text: str) -> ProcessData:
    """
    Tenta extrair todas as informações disponíveis.
    Retorna None para campos não encontrados.
    """
    # Extrair com tolerance a dados faltando
    # Permite processos parciais
```

### Estratégia 2: Strict Mode (Futuro)

```python
def parse_strict(self, text: str) -> ProcessData:
    """
    Tenta extrair todas as informações.
    Lança exceção se campos obrigatórios faltarem.
    """
    # Rigidez máxima
    # Garantia de qualidade
```

## Exemplo Prático

```python
# Uso básico
parser = Parser()
process_data = parser.parse(raw_text, source_pdf=Path("processo.pdf"))

print(f"Processo: {process_data.process_number}")
print(f"Contribuinte: {process_data.taxpayer_name}")
print(f"CPF/CNPJ: {process_data.cpf_cnpj}")
print(f"Email: {process_data.email}")
print(f"Valor da dívida: {process_data.debt_amount}")
print(f"Fundamentos legais: {len(process_data.legal_basis)}")
```

## Testes do Parser

```python
import pytest
from parser import Parser
from models import ProcessData

def test_parser_complete():
    """Testa parser com dados completos."""
    parser = Parser()
    text = "Número do processo: 123/2026. CPF: 123.456.789-00. Email: teste@example.com."
    result = parser.parse(text)
    
    assert isinstance(result, ProcessData)
    assert result.process_number == "123/2026"
    assert result.cpf_cnpj == "12345678900"
    assert result.email == "teste@example.com"

def test_parser_partial():
    """Testa parser com dados parciais."""
    parser = Parser()
    text = "Número do processo: 456/2026. CPF: 987.654.321-00."
    result = parser.parse(text)
    
    assert result.process_number == "456/2026"
    assert result.cpf_cnpj == "98765432100"
    assert result.email == ""  # Não encontrado

def test_parser_validation_error():
    """Testa parser com dados inválidos."""
    parser = Parser()
    text = "Sem dados relevantes aqui."
    
    with pytest.raises(ParseError):
        parser.parse_strict(text)
```

## Evolução Futura

1. **Multiple Parsers:** Suportar múltiplos tipos de processos
2. **Custom Rules:** Permitir regras customizadas por usuário
3. **Machine Learning:** Melhorar precisão com ML (futuro)
4. **Feedback Loop:** Aprender com correções do usuário
