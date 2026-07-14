# Prompts - GDANT

Este arquivo registra os prompts que geraram os marcos arquitetônicos importantes do projeto GDANT.

## Marco 1: Fundação do Projeto

### Prompt Original

```
Crie um leitor de texto de arquivos PDF usando PyMuPDF (fitz).

Este módulo extrai texto bruto de PDFs, preservando a ordem das páginas.
Não utiliza OCR, interpretação de texto ou extração de campos.

Crie dataclass chamada PdfPageText:
- page_number: int (começando em 1)
- text: str

Crie dataclass chamada PdfTextResult:
- file_path: Path
- pages: list[PdfPageText]
- full_text: str

Crie classe PdfReader com método read_text(pdf_path: Path) -> PdfTextResult
```

### Resultado

✅ Módulo `pdf_reader.py` criado com sucesso

---

## Marco 2: Modelo de Dados

### Prompt Original

```
Crie a estrutura de dados ProcessData.

Esta classe representará um Processo Administrativo após parsing.

Não implemente:
- Lógica de parsing
- Geração de documentos
- Regras de negócio

Apenas crie a estrutura de dados com os seguintes campos:

process_number: str = ""
taxpayer_name: str = ""
cpf_cnpj: str = ""
phone: str = ""
email: str = ""
address: str = ""
number: str = ""
complement: str = ""
district: str = ""
city: str = ""
state: str = ""
zip_code: str = ""
administrative_process: str = ""
infraction_notice: str = ""
notification_number: str = ""
notification_date: str = ""
judgment_date: str = ""
judgment_notification_date: str = ""
ar_number: str = ""
debt_amount: float = 0.0
legal_basis: list[str]
observations: list[str]

Crie __post_init__() para inicializar legal_basis e observations como listas vazias.
Use apenas dataclass.
Sem métodos além de __post_init__.
```

### Refinamentos Posteriores

1. **Refatoração de ProcessData:**
   - Remover campos duplicados
   - Substituir float por Decimal
   - Adicionar source_pdf
   - Adicionar raw_text
   - Renomear campos para clareza

2. **Type Hint de source_pdf:**
   - Mudar de `Path = None` para `Path | None = None`

### Resultado

✅ Módulo `models.py` criado e refinado

---

## Marco 3: Padrões Textuais

### Prompt Original

```
Crie novo módulo: src/patterns.py

Este módulo deve conter APENAS listas de constantes em português.

Sem funções.
Sem classes.
Sem lógica de parsing.

Crie as seguintes constantes (listas de strings):

PROCESS_NUMBER_PATTERNS = []
INFRACTION_NUMBER_PATTERNS = []
CPF_PATTERNS = []
CNPJ_PATTERNS = []
PHONE_PATTERNS = []
EMAIL_PATTERNS = []
ADDRESS_PATTERNS = []
CITY_PATTERNS = []
STATE_PATTERNS = []
ZIP_CODE_PATTERNS = []
NOTIFICATION_PATTERNS = []
JUDGMENT_PATTERNS = []
AR_PATTERNS = []
LEGAL_BASIS_PATTERNS = []

Popule cada lista com os rótulos mais comuns em português encontrados em processos administrativos brasileiros.

Não implemente regex.
Não implemente parser.
Apenas centralize padrões textuais.
```

### Resultado

✅ Módulo `patterns.py` criado com 14 constantes de padrões

---

## Marco 4: Documentação Permanente

### Prompt Original

```
Crie uma estrutura de documentação permanente para o projeto GDANT.

Crie pasta: docs/

Dentro dela, crie os seguintes arquivos:

PROJECT_STATE.md - Estado atual do projeto
CHANGELOG.md - Histórico de versões
ROADMAP.md - Planejamento futuro
TODO.md - Checklist de atividades
MANUAL_TECNICO.md - Explicação técnica do projeto
TEMPLATE_MASTER.md - Conceito de template
ARCHITECTURE.md - Arquitetura em camadas
DECISIONS.md - Decisões arquitetônicas
EXTRACTORS_GUIDE.md - Guia de desenvolvimento de extractors
PARSER_GUIDE.md - Guia do parser
SESSION_LOG.md - Log desta sessão
PROMPTS.md - Este arquivo

Popule com conteúdo significativo em português.
Escreva profissionalmente.
Mantenha conciso mas completo.
Esta documentação deve ser memória permanente do projeto.
```

### Resultado

✅ 12 documentos técnicos criados

---

## Referências

Todos os prompts foram executados em sequência para criar a fundação do projeto GDANT.

Os prompts refletem a evolução do projeto e as decisões arquitetônicas tomadas.
