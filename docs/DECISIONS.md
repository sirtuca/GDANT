# Decisões Arquitetônicas - GDANT

## Registros de Decisões

Este documento registra todas as decisões arquitetônicas importantes tomadas durante o desenvolvimento do GDANT.

### 1. Arquitetura em Camadas em vez de Abordagem Monolítica

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** Implementar arquitetura em camadas com separação clara de responsabilidades

**Justificativa:**
- Facilita testes unitários
- Permite modificações independentes
- Reduz acoplamento
- Melhora manutenibilidade

**Implicações:**
- Código dividido em múltiplos módulos
- Interface clara entre componentes
- Possibilidade de reutilização de componentes

---

### 2. Engine em vez de Processor

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** Nomear a classe orquestradora como `Engine` em vez de `Processor`

**Justificativa:**
- "Engine" melhor descreve a função de orquestração
- Evita confusão com processadores de dados
- Alinha com terminologia comum em sistemas

**Implicações:**
- Clareza semântica no código
- Melhor comunicação com stakeholders

---

### 3. QListWidget em vez de QTextEdit

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** Usar `QListWidget` na interface para seleção de PDFs

**Justificativa:**
- Melhor UX para seleção múltipla
- Interface mais clara e intuitiva
- Permite drag-and-drop futuramente
- Melhor gerenciamento de arquivos

**Implicações:**
- QTextEdit não será usado
- Interface mais amigável ao usuário

---

### 4. ProcessData como Contrato

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** Usar `ProcessData` como contrato de dados entre Parser e WordGenerator

**Justificativa:**
- Desacopla Parser de WordGenerator
- Interface clara de comunicação
- Facilita testes
- Permite evolução independente de componentes

**Implicações:**
- Parser deve preencher ProcessData
- WordGenerator consome ProcessData
- Sem dependência direta entre Parser e WordGenerator

---

### 5. PdfReader Preserva Ordem de Páginas

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** `PdfReader.read_text()` retorna páginas em ordem preservada

**Justificativa:**
- Contexto de página importante para parsing
- Alguns dados podem aparecer apenas em páginas específicas
- Melhora acurácia de extração

**Implicações:**
- Retorno estruturado por página (`PdfPageText`)
- Texto completo também disponível (`full_text`)
- Parser pode acessar página por página se necessário

---

### 6. Float Substituído por Decimal

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** Usar `Decimal` em vez de `float` para `debt_amount`

**Justificativa:**
- Precisão exata em operações monetárias
- Evita erros de arredondamento
- Padrão em aplicações financeiras
- Alinha com boas práticas

**Implicações:**
- Importação de `decimal.Decimal`
- Valores monetários precisos
- Compatibilidade com sistemas financeiros

---

### 7. Campo `raw_text` Adicionado ao ProcessData

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** Incluir campo `raw_text` em `ProcessData`

**Justificativa:**
- Rastreabilidade do processo
- Facilita debugging
- Permite re-extração futura
- Histórico completo disponível

**Implicações:**
- Armazenamento de texto completo
- Possibilita auditoria
- Melhor debugging de falhas

---

### 8. Campo `source_pdf` Adicionado ao ProcessData

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** Incluir campo `source_pdf` em `ProcessData`

**Justificativa:**
- Rastreamento da origem dos dados
- Facilita links entre processamento e fonte
- Importante para auditoria
- Permite reprocessamento seletivo

**Implicações:**
- Tipo `Path | None` para flexibilidade
- Rastreabilidade completa
- Melhor gerenciamento de processamentos

---

### 9. Padrões Textuais Centralizados em patterns.py

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** Centralizar padrões textuais em módulo `patterns.py`

**Justificativa:**
- Facilita manutenção
- Padrões em um único lugar
- Fácil atualização de regras
- Separação de dados de código

**Implicações:**
- Módulo apenas com constantes
- Extractors consultam patterns.py
- Regras podem ser alteradas sem recompilação

---

### 10. Extractors Especializados em vez de Bibliotecas de Palavras-chave

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** Implementar extractors especializados em vez de usar bibliotecas de keywords genéricas

**Justificativa:**
- Maior controle sobre extração
- Lógica específica por tipo de dado
- Melhor acurácia
- Facilita manutenção específica

**Implicações:**
- Desenvolvimento de múltiplos extractors
- Código mais específico do domínio
- Melhor qualidade de extração

---

### 11. Interface sem Lógica de Negócio

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** Interface (PyQt6) nunca contém lógica de negócio

**Justificativa:**
- Facilita testes (lógica testável sem interface)
- Permite múltiplas interfaces (CLI, Web, etc)
- Código mais limpo
- Separação clara de responsabilidades

**Implicações:**
- Validações na camada de negócio
- Interface apenas coleta e exibe
- Lógica isolada e testável

---

### 12. Engine Apenas Orquestra

**Data:** 2026-07-01  
**Status:** ✅ Aceita  
**Decisão:** `Engine` apenas orquestra, não implementa lógica de parsing ou geração

**Justificativa:**
- Responsabilidade única
- Fácil manutenção
- Fácil testes
- Componentes independentes

**Implicações:**
- Parser é chamado pelo Engine
- WordGenerator é chamado pelo Engine
- Engine não contém lógica complexa

---

## Próximas Decisões Esperadas

- Escolha entre python-docx vs ReportLab para geração de documentos
- Estratégia de cache para PDFs processados
- Abordagem de versionamento de templates
- Integração com sistemas de fila de processamento
