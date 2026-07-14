# Estado do Projeto GDANT

## Informações Gerais

**Versão:** 0.1.0  
**Sprint Atual:** Sprint 4  
**Status Geral:** Em Desenvolvimento  
**Data de Início:** 2026-07-01

## Módulos Concluídos

- ✅ **pdf_reader.py** - Leitura de texto de arquivos PDF usando PyMuPDF
- ✅ **models.py** - Estrutura de dados ProcessData para contrato entre parser e gerador
- ✅ **patterns.py** - Padrões textuais em português para extração de dados

## Status da Arquitetura

```
Interface (PyQt6)
    ↓
Engine (Orquestração)
    ↓
PdfReader (Extração de Texto)
    ↓
Extractors (Especializados)
    ↓
Parser (Assembla ProcessData)
    ↓
ProcessData (Contrato)
    ↓
WordGenerator (Preenche Template)
    ↓
PdfGenerator (Gera PDF Final)
```

## Próxima Sprint (Sprint 5)

- Criar módulo de Extractors especializados
- Implementar Parser
- Criar testes unitários

## Papéis do Time

- **Desenvolvedor Principal:** sirtuca
- **Arquiteto:** sirtuca
- **Documentador:** sirtuca

## Princípios Arquitetônicos

1. Interface sem regras de negócio
2. Engine apenas orquestra
3. PdfReader preserva ordem de páginas
4. Cada Extractor extrai uma informação específica
5. Parser constrói ProcessData a partir de Extractors
6. ProcessData é o contrato entre Parser e WordGenerator
7. Arquitetura simples preferida sobre complexidade
