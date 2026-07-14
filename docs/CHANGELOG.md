# Changelog - GDANT

## [0.1.0] - 2026-07-01

### Sprint 4 - Fundação do Projeto

#### Adicionado
- ✅ Módulo `pdf_reader.py` com classe PdfReader para extração de texto de PDFs
- ✅ Estrutura de dados `ProcessData` como dataclass
- ✅ Módulo `patterns.py` com constantes de padrões textuais em português
- ✅ Documentação técnica completa do projeto

#### Modificado
- ✅ Refinamento do ProcessData com campos consolidados
- ✅ Substituição de `float` por `Decimal` para valores monetários
- ✅ Renomeação de campos para clareza: `infraction_notice` → `infraction_number`
- ✅ Adição de campos de origem: `source_pdf`, `raw_text`

#### Removido
- ✅ Campo duplicado `administrative_process` do ProcessData
- ✅ Componentes desnecessários do modelo inicial

### Inicialização do Projeto

- Criação do repositório GDANT no GitHub
- Setup da estrutura básica do projeto
- Definição da arquitetura em camadas
- Documentação da filosofia do projeto
