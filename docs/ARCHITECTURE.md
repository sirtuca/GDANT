# Arquitetura - GDANT

## Diagrama em Camadas

```
┌─────────────────────────────────────────────┐
│         Interface (PyQt6)                   │
│  - QListWidget para seleção de PDFs        │
│  - Menu e configurações                     │
│  - Visualização de resultados               │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Engine                              │
│  - Orquestra todo o fluxo                  │
│  - Coordena processamento                   │
│  - Gerencia estado                          │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         PdfReader                           │
│  - Extrai texto bruto do PDF               │
│  - Preserva ordem de páginas                │
│  - Retorna texto por página                 │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Extractors                          │
│  - ExtractorCpf                            │
│  - ExtractorCnpj                           │
│  - ExtractorEmail                          │
│  - ExtractorPhone                          │
│  - ExtractorProcessNumber                  │
│  - ... (um para cada tipo de dado)         │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Parser                              │
│  - Assembla ProcessData                    │
│  - Coordena Extractors                      │
│  - Valida dados                             │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         ProcessData                         │
│  - Contrato de dados entre Parser e         │
│    WordGenerator                            │
│  - Estrutura de dados consolidada           │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         WordGenerator                       │
│  - Preenche Template Mestre                │
│  - Substitui placeholders                   │
│  - Formata listas e dados                   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         PdfGenerator                        │
│  - Converte documento para PDF              │
│  - Otimiza para impressão                   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│    Documento Final (PDF)                    │
└─────────────────────────────────────────────┘
```

## Componentes Principais

### 1. Interface (PyQt6)

**Responsabilidade:** Interação com usuário

**Restrições:**
- ❌ Nunca contém lógica de negócio
- ❌ Nunca valida dados diretamente
- ❌ Nunca faz parsing
- ✅ Apenas coleta entrada e exibe resultado

### 2. Engine

**Responsabilidade:** Orquestração do fluxo

**Operações:**
- Coordena leitura de PDF
- Dispara extractors
- Invoca parser
- Chama generators
- Gerencia estado do processamento

**Restrições:**
- ❌ Nunca extrai dados diretamente
- ❌ Nunca contém regras de negócio
- ✅ Apenas orquestra componentes

### 3. PdfReader

**Responsabilidade:** Leitura de texto de PDF

**Operações:**
- Abre arquivo PDF
- Extrai texto de cada página
- Preserva ordem de páginas
- Retorna estrutura de dados com texto

**Restrições:**
- ❌ Nunca interpreta dados
- ❌ Nunca usa OCR
- ✅ Apenas extrai texto bruto

### 4. Extractors

**Responsabilidade:** Extração especializada de um tipo de dado

**Padrão de cada Extractor:**
```python
class Extractor:
    def extract(text: str) -> value:
        # Recebe texto bruto
        # Busca padrões (patterns.py)
        # Extrai e limpa o valor
        # Retorna um único valor tipado
```

**Restrições:**
- ❌ Um extractor = uma responsabilidade
- ❌ Nunca validam regras de negócio complexas
- ✅ Apenas extraem e limpam dados

### 5. Parser

**Responsabilidade:** Assembla ProcessData

**Operações:**
- Coordena múltiplos extractors
- Assembla ProcessData com resultados
- Valida coerência entre campos
- Retorna ProcessData completo

**Restrições:**
- ❌ Nunca implementa regras de negócio específicas do domínio
- ✅ Apenas constrói a estrutura de dados

### 6. ProcessData

**Responsabilidade:** Contrato de dados

**Características:**
- Dataclass simples
- Sem métodos (apenas __post_init__)
- Tipagem completa
- Documentação em cada campo

### 7. WordGenerator

**Responsabilidade:** Preenchimento de template

**Operações:**
- Recebe ProcessData
- Carrega Template Mestre
- Substitui placeholders
- Retorna documento Word

**Restrições:**
- ❌ Nunca extrai dados
- ✅ Apenas preenche template

### 8. PdfGenerator

**Responsabilidade:** Conversão para PDF

**Operações:**
- Recebe documento Word
- Converte para PDF
- Otimiza para impressão
- Retorna arquivo PDF

## Princípios de Design

### 1. Single Responsibility Principle (SRP)

Cada classe/função tem uma única responsabilidade bem definida.

### 2. Dependency Inversion

Componentes dependem de abstrações, não de implementações concretas.

### 3. Contract-Based Design

ProcessData é o contrato entre Parser e WordGenerator.

### 4. Testabilidade

Cada componente é testável isoladamente:

```python
# Testa PdfReader independentemente
text = pdf_reader.read("test.pdf")

# Testa Extractor com texto de exemplo
email = extractor_email.extract(text)

# Testa Parser com dados de exemplo
process_data = parser.parse(text)

# Testa WordGenerator com ProcessData de exemplo
document = word_generator.generate(process_data)
```

### 5. Documentação como Código

Regras de negócio são documentadas em:
- `patterns.py` - Padrões textuais
- `MANUAL_TECNICO.md` - Regras de negócio
- Docstrings - Documentação inline

## Fluxo de Dados

```
PDF Input
   ↓
[PdfReader] → raw_text: str
   ↓
[Extractors] → extracted_values: dict
   ↓
[Parser] → ProcessData
   ↓
[WordGenerator] → Document (.docx)
   ↓
[PdfGenerator] → Output PDF
```

## Escalabilidade

A arquitetura suporta:

1. **Novos Extractors:** Adicionar sem modificar existentes
2. **Novos Templates:** Registrar no WordGenerator
3. **Novos Tipos de Processo:** Criar novo Parser específico
4. **Múltiplos Formatos:** Adicionar novo Generator (HTML, Excel, etc)
