# AI HANDOFF

## Objetivo do Projeto

O GDANT (Gerador de Documentos Administrativos Notificatórios) é um software desktop para gerar automaticamente **Termos de Inscrição em Dívida Ativa** a partir de Processos Administrativos em PDF.

### Escopo Principal

- **Entrada:** PDFs de Processos Administrativos
- **Processamento:** Extração inteligente de dados
- **Saída:** Documentos Word/PDF padronizados prontos para uso

### Filosofia de Desenvolvimento

O foco é:

- **Velocidade:** Interface responsiva, processamento rápido
- **Simplicidade:** Código limpo, sem over-engineering
- **Estabilidade:** Poucos bugs, fácil manutenção
- **Evolução:** Preparado para mudanças futuras sem reescritas

---

## Filosofia

O projeto **NÃO** busca criar um software complexo com soluções sofisticadas.

Toda decisão deve privilegiar:

- ✅ **Simplicidade** - Código direto, sem padrões desnecessários
- ✅ **Clareza** - Fácil entender o que cada módulo faz
- ✅ **Manutenção Fácil** - Uma pessoa consegue manter sozinha
- ✅ **Baixo Acoplamento** - Módulos independentes e testáveis
- ✅ **Alta Legibilidade** - Novos desenvolvedores entendem rapidamente

### Regra de Ouro

**Sempre preferir código simples.**

Dúvida entre duas abordagens? Escolher a mais simples.

Dúvida entre uma feature ou simplicidade? Escolher simplicidade.

---

## Arquitetura

```
┌─────────────────────────────────┐
│     Interface (PyQt6)           │
│  - QListWidget para PDFs        │
│  - Menu e visualização          │
│  - Sem lógica de negócio        │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│         Engine                  │
│  - Orquestra o fluxo            │
│  - Coordena componentes         │
│  - Sem lógica específica        │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│      PdfReader                  │
│  - Extrai texto de PDF          │
│  - Preserva ordem de páginas    │
│  - Retorna estrutura de dados   │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│      Extractors                 │
│  - Módulos independentes        │
│  - Um tipo de dado por módulo   │
│  - Especializados e simples     │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│       Parser                    │
│  - Coordena Extractors          │
│  - Monta ProcessData            │
│  - Valida dados                 │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│    ProcessData                  │
│  - Contrato entre Parser e      │
│    WordGenerator                │
│  - Dataclass simples            │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│   WordGenerator                 │
│  - Preenche Template Mestre     │
│  - Substitui placeholders       │
│  - Retorna documento Word       │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│    PdfGenerator                 │
│  - Converte para PDF            │
│  - Otimiza para impressão       │
│  - Retorna PDF final            │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│   Documento Final (PDF)         │
└─────────────────────────────────┘
```

### Responsabilidade de Cada Módulo

**Interface:** Coleta entrada do usuário e exibe resultado. Nunca contém lógica de negócio.

**Engine:** Orquestra o fluxo chamando componentes na sequência correta. Não implementa lógica específica.

**PdfReader:** Extrai texto bruto de PDFs preservando ordem de páginas. Apenas leitura, sem interpretação.

**Extractors:** Módulos especializados e independentes, cada um responsável por extrair um tipo específico de informação. Reutilizáveis, testáveis e sem dependências entre si. A lógica de cada extractor é tailored para seu tipo de dado.

**Parser:** Coordena múltiplos Extractors e monta ProcessData. Valida coerência entre campos.

**ProcessData:** Dataclass que representa um processo completamente extraído. Contrato entre Parser e WordGenerator.

**WordGenerator:** Recebe ProcessData e preenche placeholders no Template Mestre. Apenas preenchimento, sem transformações.

**PdfGenerator:** Converte documento Word em PDF otimizado para impressão.

---

## Regras Permanentes

### 1. Separação de Responsabilidades

```
❌ NUNCA: colocar lógica de Parser em Engine
❌ NUNCA: colocar lógica de Extractor em Parser
❌ NUNCA: colocar lógica de WordGenerator em Engine
✅ SEMPRE: cada módulo tem uma responsabilidade única
```

### 2. Regras Jurídicas

```
❌ NUNCA colocar regra jurídica na Interface
❌ NUNCA colocar regra jurídica no Engine
✅ SEMPRE documentar regras em MANUAL_TECNICO.md
✅ SEMPRE implementar regras em Extractors
```

### 3. ProcessData

```
✅ ProcessData é o contrato OFICIAL entre Parser e WordGenerator
✅ Nenhum outro módulo deve ser contrato entre componentes
✅ ProcessData é uma dataclass pura (sem métodos complexos)
✅ Todos os campos devem estar documentados
```

### 4. Fluxo de Dados

```
Parser MONTA ProcessData
    ↓
WordGenerator CONSOME ProcessData
    ↓
Sem acoplamento direto entre Parser e WordGenerator
```

### 5. Extractors Independentes

```
✅ Cada Extractor é um módulo independente
✅ Extractors não chamam outros Extractors
✅ Lógica de cada Extractor é isolada
✅ Fácil adicionar novos Extractors sem modificar existentes
```

---

## Evolução

Quando surgir uma **nova regra de negócio** ou requisito:

### Passo 1: Registrar em DECISIONS.md

```
Documentar:
- O que é a nova regra
- Por que foi adicionada
- Como impacta a arquitetura
- Implica de outros componentes
```

### Passo 2: Atualizar MANUAL_TECNICO.md

```
Explicar:
- Qual é a nova regra
- Quando se aplica
- Exemplos de uso
```

### Passo 3: Implementar ou Atualizar Extractor

```
Se for novo tipo de dado:
- Criar novo Extractor especializado
- Implementar lógica específica
- Escrever testes

Se for modificação em tipo existente:
- Atualizar Extractor correspondente
- Manter compatibilidade com Parser
- Atualizar testes
```

### Passo 4: Atualizar SESSION_LOG.md

```
Registrar:
- O que foi implementado
- Commits relacionados
- Impacto no código
```

**Nunca começar implementação sem passar pelos passos 1-3.**

---

## Continuação do Projeto

### Antes de Escrever Qualquer Código

Leitura OBRIGATÓRIA nesta ordem:

1. **PROJECT_STATE.md** - Entender estado atual do projeto
2. **DECISIONS.md** - Conhecer decisões arquitetônicas tomadas
3. **ARCHITECTURE.md** - Entender a estrutura completa
4. **MANUAL_TECNICO.md** - Conhecer regras de negócio
5. **SESSION_LOG.md** - Saber o que foi feito e próximas ações
6. **TODO.md** - Prioridades de desenvolvimento

Somente depois abrir o código-fonte.

### Fluxo de Trabalho

```
1. Ler documentação obrigatória (acima)
2. Abrir PROJECT_STATE.md
3. Verificar próxima sprint em TODO.md
4. Consultar ARCHITECTURE.md para contexto
5. Ler DECISIONS.md relacionadas
6. Implementar seguindo as regras
7. Atualizar SESSION_LOG.md e DECISIONS.md
8. Fazer commit com mensagem clara
```

### Dúvidas Arquitetônicas

Quando surgir dúvida sobre como implementar algo:

1. Consultar DECISIONS.md para decisões similares
2. Consultar ARCHITECTURE.md para padrão
3. Consultar EXTRACTORS_GUIDE.md se for Extractor
4. Consultar PARSER_GUIDE.md se for Parser
5. Quando em dúvida: escolher a opção mais simples

---

## Documentação Como Código

A documentação NÃO é luxo. É essencial.

### Manter Sincronizado

Quando modificar código:

```
❌ NUNCA: modificar código sem atualizar documentação
✅ SEMPRE: commit atualiza código E documentação
```

### Padrão de Documentação

```
1. DECISIONS.md - decisão arquitetônica
2. Docstring no código - explicação inline
3. SESSION_LOG.md - o que foi feito
4. Commit message - resumo da mudança
```

---

## Princípio Fundamental

### O Verdadeiro Objetivo

O objetivo do GDANT **não é apenas gerar documentos**.

O objetivo é criar um **motor documental capaz de evoluir durante anos** sem necessidade de reescrever o software.

### Como Alcançar

- ✅ Manter arquitetura simples
- ✅ Baixo acoplamento entre módulos
- ✅ Documentação permanente
- ✅ Decisões registradas
- ✅ Separação clara de responsabilidades
- ✅ ProcessData como contrato
- ✅ Extractors especializados e independentes

### Teste de Qualidade

Quando implementar uma feature, pergunte:

> "Se eu adicionar 10 novos tipos de processos no futuro, esse código continuará funcionando sem mudanças drásticas?"

Se a resposta for **não**, refatorar antes de fazer commit.

---

## Status Atual

**Data:** 2026-07-01  
**Status:** Fundação Completa (Sprint 4)  
**Módulos Completados:** PdfReader, ProcessData, Documentação Técnica

---

## Próxima Sprint

**Sprint 5 - Extractors e Parser**

- Implementar Extractors especializados
- Criar Parser que coordena Extractors
- Testes unitários completos
- Validação com PDFs de exemplo

Bem-vindo ao projeto GDANT! 🚀
