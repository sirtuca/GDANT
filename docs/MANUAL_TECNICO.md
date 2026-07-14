# Manual Técnico - GDANT

## Propósito do GDANT

GDANT (Gerador de Documentos Administrativos Notificatórios) é uma ferramenta que automatiza a extração de dados de Processos Administrativos em PDF e a geração de documentos padronizados baseados em Templates Mestres.

### Objetivo Principal

Reduzir o tempo manual de extração de informações de processos administrativos brasileiros e padronizar a geração de documentos de notificação.

## Workflow

```
1. Usuário carrega PDF de Processo Administrativo
       ↓
2. PdfReader extrai texto bruto preservando ordem de páginas
       ↓
3. Extractors especializam dados específicos (CPF, Email, etc)
       ↓
4. Parser assembla ProcessData com todos os dados extraídos
       ↓
5. WordGenerator preenche Template Mestre com dados do ProcessData
       ↓
6. PdfGenerator converte documento para PDF final
       ↓
7. Usuário recebe documento formatado e pronto para uso
```

## Filosofia do Projeto

### 1. Separação de Responsabilidades

Cada módulo tem uma responsabilidade única e bem definida:

- **PdfReader:** Apenas lê texto
- **Extractors:** Apenas extraem um tipo de dado
- **Parser:** Apenas assembla ProcessData
- **WordGenerator:** Apenas preenche template
- **Engine:** Apenas orquestra o fluxo

### 2. Interface sem Lógica de Negócio

A interface gráfica (PyQt6) nunca contém lógica de negócio:

- Validações ocorrem nos Extractors
- Transformações ocorrem no Parser
- Interface apenas exibe e coleta dados

### 3. Regras de Negócio através de Documentação

Em vez de hardcodificar regras de negócio no código:

- Regras são documentadas em `patterns.py` (padrões textuais)
- Regras são explicadas em `MANUAL_TECNICO.md`
- Extractors são parametrizáveis através de padrões
- Futuras mudanças nas regras não exigem recompilação

### 4. Contratos Claros

ProcessData atua como contrato entre Parser e WordGenerator:

- Parser preenche ProcessData
- WordGenerator consome ProcessData
- Sem acoplamento direto entre componentes

### 5. Simplicidade Preferida

- Arquitetura simples e direta
- Sem padrões complexos desnecessários
- Fácil de entender e manter

## Escalabilidade Futura

A arquitetura foi desenhada para suportar:

- Múltiplos tipos de processos
- Múltiplos templates mestres
- Múltiplos formatos de saída
- Integração com sistemas legados
- Validação automática de dados
