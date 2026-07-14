# START HERE

## Bem-vindo ao GDANT

Este documento é o **ponto de partida obrigatório** para qualquer desenvolvedor ou assistente de IA que deseje continuar desenvolvendo o GDANT.

O GDANT (Gerador de Documentos Administrativos Notificatórios) é um software desktop que automatiza a geração de Termos de Inscrição em Dívida Ativa a partir de Processos Administrativos em PDF.

**Se esta é sua primeira vez aqui, siga exatamente a ordem de leitura abaixo.**

---

## Ordem Obrigatória de Leitura

Antes de abrir qualquer arquivo de código, leia **exatamente nesta ordem**:

1. **docs/AI_HANDOFF.md** - Filosofia e princípios do projeto
2. **docs/PROJECT_STATE.md** - Estado atual e módulos completados
3. **docs/DECISIONS.md** - Decisões arquitetônicas registradas
4. **docs/ARCHITECTURE.md** - Arquitetura em camadas explicada
5. **docs/MANUAL_TECNICO.md** - Regras de negócio e workflow
6. **docs/SESSION_LOG.md** - O que foi feito e próximas ações
7. **docs/TODO.md** - Prioridades de desenvolvimento

**Somente depois** abra a pasta `src/` para ver o código-fonte.

---

## Objetivo do Projeto

O GDANT é um software **desktop** que gera automaticamente **Termos de Inscrição em Dívida Ativa** a partir de Processos Administrativos em PDF.

### Filosofia de Desenvolvimento

O projeto prioriza:

- ✅ **Simplicidade** - Código direto, sem over-engineering
- ✅ **Velocidade** - Interface responsiva, processamento rápido
- ✅ **Baixo Acoplamento** - Módulos independentes e testáveis
- ✅ **Fácil Evolução** - Preparado para mudanças futuras sem reescrita

### Não é o Objetivo

- ❌ Criar o software mais complexo
- ❌ Usar padrões sofisticados desnecessários
- ❌ Implementar tudo de uma vez
- ❌ Mudar a arquitetura a cada novo requisito

---

## Estado Atual

**Sprint:** 4 - Fundação Completa  
**Data:** 2026-07-01

### Módulos Implementados

- ✅ **Interface** - Estrutura básica com PyQt6
- ✅ **Configuração Persistente** - Salvamento de preferências
- ✅ **Engine** - Orquestração do fluxo
- ✅ **Scanner de PDFs** - Detecção e carregamento de arquivos
- ✅ **PdfReader** - Extração de texto preservando ordem de páginas
- ✅ **ProcessData** - Estrutura de dados (contrato entre Parser e WordGenerator)
- ✅ **Documentação Consolidada** - 13 arquivos técnicos

### Arquitetura Atual

```
Interface → Engine → PdfReader → Extractors → Parser → ProcessData → WordGenerator → PdfGenerator
```

---

## Próxima Sprint

**Sprint 5 - Extractors e Parser**

### O que Fazer

1. Criar módulo de **Extractors especializados**
   - Um extractor por tipo de dado (CPF, Email, Telefone, etc)
   - Módulos independentes e testáveis

2. Implementar **Parser** que coordena Extractors
   - Monta ProcessData com dados extraídos
   - Valida coerência entre campos

3. Escrever **testes unitários**
   - Testes para cada extractor
   - Testes de integração do parser

4. Validar com **PDFs reais**
   - Testar com processos administrativos de exemplo
   - Refinar lógica de extração

### O que NÃO Fazer

- ❌ Não implementar WordGenerator ainda
- ❌ Não implementar PdfGenerator ainda
- ❌ Não pular etapas
- ❌ Não modificar arquitetura sem registrar em DECISIONS.md

---

## Como Trabalhar

### Ciclo de Desenvolvimento

Sempre seguir **esta ordem**:

```
1. LER A DOCUMENTAÇÃO (docs/)
   ↓
2. ENTENDER A SPRINT ATUAL (docs/TODO.md)
   ↓
3. IMPLEMENTAR APENAS UMA SPRINT POR VEZ
   ↓
4. ATUALIZAR A DOCUMENTAÇÃO
   ↓
5. FAZER COMMIT
   ↓
6. REPITA PARA A PRÓXIMA SPRINT
```

### Regras Importantes

- ✅ Uma sprint por vez
- ✅ Documentar antes de implementar
- ✅ Atualizar DECISIONS.md se houver mudanças arquitetônicas
- ✅ Atualizar SESSION_LOG.md após implementar
- ✅ Escrever testes enquanto implementa
- ✅ Fazer commits pequenos e descritivos

- ❌ Nunca pular etapas
- ❌ Nunca implementar múltiplas sprints simultaneamente
- ❌ Nunca modificar código sem atualizar documentação
- ❌ Nunca fazer huge commits

### Ao Ter Dúvida

1. Consulte **docs/ARCHITECTURE.md** para entender estrutura
2. Consulte **docs/DECISIONS.md** para decisões similares
3. Consulte **docs/EXTRACTORS_GUIDE.md** para criar novo extractor
4. Consulte **docs/PARSER_GUIDE.md** para entender parser
5. Quando tiver dúvida: **escolha a opção mais simples**

---

## Filosofia

### O Verdadeiro Objetivo

O objetivo do GDANT **não é apenas gerar documentos**.

O objetivo é criar um **software capaz de evoluir durante muitos anos** sem necessidade de reescrever o código do zero.

### Como Alcançar Isso

- ✅ Manter arquitetura simples e clara
- ✅ Documentar todas as decisões importantes
- ✅ Manter baixo acoplamento entre módulos
- ✅ Cada módulo tem uma responsabilidade única
- ✅ Usar ProcessData como contrato entre componentes
- ✅ Escrever testes para cada feature
- ✅ Revisar código regularmente

### Teste Pessoal

Quando implementar algo, pergunte-se:

> "Se eu precisar adicionar 10 novos tipos de processos em 2 anos, esse código continuará funcionando sem mudanças drásticas?"

Se a resposta for **não**, refatore antes de fazer commit.

---

## Continuidade do Projeto

Este documento existe para garantir que **qualquer IA** (ChatGPT, GitHub Copilot, Cursor, Claude ou outra) consiga continuar o projeto exatamente do ponto em que foi interrompido.

### Se Você é uma IA

Bem-vindo! Aqui está o que fazer:

1. Leia os 7 documentos na ordem acima
2. Abra `docs/TODO.md` e veja qual é a próxima sprint
3. Consulte `docs/SESSION_LOG.md` para entender o contexto
4. Abra `src/` e comece a implementar
5. Sempre mantenha a documentação sincronizada com o código
6. Registre suas decisões em `docs/DECISIONS.md`
7. Faça um novo entry em `docs/SESSION_LOG.md` quando terminar

### Se Você é um Desenvolvedor Humano

O mesmo aplica! A documentação é para você também. Não é sobre AI vs humano, é sobre **continuidade e clareza**.

---

## Estrutura do Repositório

```
GDANT/
├── src/
│   ├── models.py          # ProcessData e estruturas de dados
│   ├── pdf_reader.py      # Leitura de PDFs
│   └── [outros módulos]
│
├── docs/
│   ├── START_HERE.md          # ← Você está aqui
│   ├── AI_HANDOFF.md          # Filosofia e princípios
│   ├── PROJECT_STATE.md       # Estado do projeto
│   ├── ARCHITECTURE.md        # Arquitetura explicada
│   ├── DECISIONS.md           # Decisões registradas
│   ├── MANUAL_TECNICO.md      # Regras de negócio
│   ├── SESSION_LOG.md         # O que foi feito
│   ├── TODO.md                # Próximas tarefas
│   ├── ROADMAP.md             # Visão de longo prazo
│   ├── EXTRACTORS_GUIDE.md    # Como criar extractors
│   ├── PARSER_GUIDE.md        # Como criar parser
│   ├── TEMPLATE_MASTER.md     # Conceito de template
│   ├── CHANGELOG.md           # Histórico de versões
│   └── PROMPTS.md             # Prompts originais
│
├── tests/
│   └── [testes unitários]
│
└── README.md
```

---

## Próximos Passos

### Agora

1. Feche este arquivo
2. Abra **docs/AI_HANDOFF.md**
3. Leia nesta ordem: AI_HANDOFF → PROJECT_STATE → DECISIONS → ARCHITECTURE → MANUAL_TECNICO → SESSION_LOG → TODO
4. Depois, abra `src/` para entender o código existente

### Depois

1. Escolha a próxima sprint em **docs/TODO.md**
2. Abra **docs/EXTRACTORS_GUIDE.md** (você vai precisar)
3. Comece a implementar
4. Atualize a documentação conforme avança
5. Faça commits bem documentados

---

## Contato e Referências

- **Projeto Original:** GDANT
- **Sprint Atual:** 5 - Extractors e Parser
- **Documentação:** `/docs`
- **Código-fonte:** `/src`
- **Testes:** `/tests`

---

**Bem-vindo ao GDANT! 🚀**

Você está no lugar certo. Leia a documentação e comece a desenvolver.

Se tiver dúvida: consulte a documentação antes de modificar o código.
