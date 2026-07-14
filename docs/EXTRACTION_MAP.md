# EXTRACTION MAP

## Introdução

Este documento mapeia como GDANT **lê e utiliza** o Template Mestre e o Manual Técnico para determinar quais dados extrair.

**Importante:** Este mapa é parametrizado. Não é hardcodado no código.

---

## Fluxo de Determinação de Campos

```
Template Mestre (DOCX)
    ↓ Sprint 7: TemplateMestre identifica merge fields
    ↓
Campos Necessários: ["PROC", "AI", "NOME", "VALOR", "DT"]
    ↓ Sprint 8: ManualTecnico mapeia para extractors
    ↓
Manual Técnico (DOCX)
    ↓
Mapeamento: 
    - PROC → extract_process_number
    - AI → extract_infraction_number
    - NOME → extract_taxpayer_name
    - VALOR → extract_debt_amount
    - DT → extract_date
    ↓ Sprint 6-9: Parser executa extractors
    ↓
ProcessData: {process_number: "...", ...}
    ↓ Sprint 9: WordGenerator preenche
    ↓
DOCX Preenchido
```

---

## Fontes de Dados (Dentro do PDF)

### Auto de Infração

Documento dentro do processo que contém:
- Nome do contribuinte
- CPF/CNPJ
- Inscrição Econômica (IE)
- Endereço completo
- Telefone
- Email
- Número da infração
- Data da infração
- Fundamento legal

### DILT Dispatch

Documento que contém:
- Código da Dívida (COD)
- Natureza da dívida
- Valor da dívida
- Data de vencimento
- Modalidade de lançamento

### Outros Documentos

- AR (Aviso de Recebimento)
- Email de notificação
- WhatsApp
- Edital
- Intimação

---

## Estratégia de Extração

### Parametrizada

Cada campo vem com **metadados** do Manual Técnico:

```
{
    "NOME": {
        "source": "auto_de_infraçao",
        "pattern": "CONTRIBUINTE",
        "extractor": "extract_taxpayer_name",
        "required": True,
        "type": "text",
    }
}
```

### Extractors São Genéricos

Um extractor **não sabe** para qual campo está trabalhando:

```python
# ✅ Certo
def extract_process_number(text: str) -> str:
    """Extrai qualquer número SEI no formato XXXXXX/YYYY-ZZ"""
    # Busca padrão, retorna valor ou ""

# ❌ Errado  
def extract_process_number_for_gdant(text: str) -> str:
    """Extrai número SEI especificamente para campo PROC"""
    # Acoplado ao template
```

---

## Exemplo Completo

### Template Mestre Tem

```
«PROC» «AI» «NOME» «VALOR» «DT»
```

### Sprint 7 Identifica

```python
required_fields = ["PROC", "AI", "NOME", "VALOR", "DT"]
```

### Manual Técnico Define

```
| Campo | Fonte | Extractor | Obrigatório |
| PROC | Header | extract_process_number | Sim |
| AI | Auto de Infração | extract_infraction_number | Sim |
| NOME | Auto de Infração | extract_taxpayer_name | Sim |
| VALOR | DILT | extract_debt_amount | Sim |
| DT | DILT | extract_due_date | Sim |
```

### Sprint 8 Mapeia

```python
extraction_rules = {
    "PROC": {
        "source": "header",
        "extractor": "extract_process_number"
    },
    "AI": {
        "source": "auto_de_infraçao",
        "extractor": "extract_infraction_number"
    },
    # ... etc
}
```

### Sprint 6-8 Executa

```python
# Parser recebe extraction_rules
pdf_text = pdf_reader.read("processo.pdf")

process_data = ProcessData()
for field, rule in extraction_rules.items():
    source_text = extract_source(pdf_text, rule["source"])
    extractor_func = get_extractor(rule["extractor"])
    value = extractor_func(source_text)
    process_data.set_field(field, value)
```

### Sprint 9 Preenche

```python
# WordGenerator recebe template + process_data
word_doc = Document("template_mestre.docx")
for field_name, field_value in process_data.items():
    word_doc.merge_fields[field_name] = field_value
word_doc.save("resultado.docx")
```

---

## Status da Implementação

### Implementado ✅

- **Sprint 6:** Extractors básicos + Parser
  - extract_process_number
  - extract_infraction_number
  - extract_cpf_cnpj

### Planejado ⏳

- **Sprint 7:** Leitura de Template Mestre
- **Sprint 8:** Leitura de Manual Técnico
- **Sprint 9:** WordGenerator para preenchimento
- **Sprint 10:** Batch processing
- **Sprint 11:** PDF generation

### Próximos Extractors (Conforme Necessário)

Baseados em qual Template Mestre o usuário escolher:

- extract_taxpayer_name
- extract_address
- extract_city
- extract_state
- extract_zip_code
- extract_phone
- extract_email
- extract_debt_amount
- extract_cod
- extract_due_date
- extract_infraction_date
- extract_legal_basis
- extract_legal_article
- ... e mais conforme necessário

---

## Importância da Parametrização

### Sem Parametrização (❌ ERRADO)

```python
def process_gdant_document(pdf):
    text = read_pdf(pdf)
    proc = extract_process_number(text)      # Hardcoded
    ai = extract_infraction_number(text)     # Hardcoded
    nome = extract_taxpayer_name(text)       # Hardcoded
    valor = extract_debt_amount(text)        # Hardcoded
    # ...
    return ProcessData(proc, ai, nome, valor)
```

**Problema:** Para cada novo template, precisamos modificar código.

### Com Parametrização (✅ CERTO)

```python
def process_document(pdf, template_mestre, manual_tecnico):
    fields = read_template_merge_fields(template_mestre)
    rules = read_manual_extraction_rules(manual_tecnico)
    
    text = read_pdf(pdf)
    process_data = ProcessData()
    
    for field in fields:
        rule = rules[field]
        extractor = get_extractor(rule["extractor"])
        value = extractor(text)
        process_data.set_field(field, value)
    
    return process_data
```

**Vantagem:** Qualquer template, qualquer manual, mesmo código.

---

## Regras de Ouro

1. **Extractors são genéricos**
   - Não sabem de templates ou manuais
   - Recebem texto, retornam valor

2. **Mapeamento vem dos documentos**
   - Template define campos obrigatórios
   - Manual define como extrair cada campo

3. **Parser coordena**
   - Não toma decisões
   - Segue as regras

4. **Sem surpresas**
   - Se um extractor não encontra valor, retorna ""
   - Sem exceções, sem crashes
   - Template e manual decidem o que fazer

---

## Próximos Passos

1. **Sprint 7:** Implementar TemplateMestre para ler DOCX
2. **Sprint 8:** Implementar ManualTecnico para ler regras
3. **Sprint 9:** Conectar tudo no Engine
4. **Sprint 10+:** Expandir extractors conforme necessário

---

**Atualizado:** 2026-07-01  
**Modelo:** Parametrizado (não hardcoded)
