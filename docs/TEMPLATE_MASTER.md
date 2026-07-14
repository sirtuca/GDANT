# Template Mestre - GDANT

## Conceito

O Template Mestre (ou Template Master) é o documento modelo em formato Word (.docx) que será preenchido com dados extraídos de Processos Administrativos.

## Estrutura

O Template Mestre contém:

1. **Estrutura Visual** - Formatação, logos, cabeçalhos e rodapés
2. **Placeholders** - Marcadores para dados dinâmicos
3. **Seções Fixas** - Textos padrão que não mudam
4. **Seções Dinâmicas** - Que variam de acordo com os dados

## Placeholders

Os placeholders no template são identificados por chaves duplas:

```
{{CAMPO_NAME}}
```

### Placeholders Suportados

```
{{PROCESS_NUMBER}}          - Número do processo
{{TAXPAYER_NAME}}           - Nome do contribuinte
{{CPF_CNPJ}}                - CPF ou CNPJ
{{PHONE}}                   - Telefone
{{EMAIL}}                   - Email
{{ADDRESS}}                 - Endereço completo
{{CITY}}                    - Cidade
{{STATE}}                   - Estado (UF)
{{ZIP_CODE}}                - CEP
{{INFRACTION_NUMBER}}       - Número da infração
{{NOTIFICATION_DATE}}       - Data da notificação
{{JUDGMENT_DATE}}           - Data do julgamento
{{JUDGMENT_NOTIFICATION_DATE}} - Data de notificação do julgamento
{{AR_NUMBER}}               - Número do AR
{{DEBT_AMOUNT}}             - Valor da dívida
{{LEGAL_BASIS}}             - Fundamentos legais (lista)
{{OBSERVATIONS}}            - Observações (lista)
{{CURRENT_DATE}}            - Data atual de geração
```

## Versioning de Templates

Futuras versões do GDANT suportarão múltiplos templates:

```
templates/
├── template_v1.docx        - Versão padrão
├── template_v2.docx        - Com melhorias
└── template_custom.docx    - Customizado por cliente
```

O `WordGenerator` permitirá selecionar qual template usar.

## Características Especiais

### Listas Dinâmicas

Para campos como `legal_basis` e `observations`:

```
Fundamentos Legais:
{{LEGAL_BASIS_ITEM}}
```

O generator criará linhas para cada item da lista.

### Formatação Condicional

Futuras versões suportarão:

```
{{IF DEBT_AMOUNT > 0}}
Valor da dívida: {{DEBT_AMOUNT}}
{{ENDIF}}
```

## Criação de Novo Template

1. Criar documento Word
2. Adicionar placeholders `{{CAMPO_NAME}}`
3. Manter formatação consistente
4. Salvar como `.docx`
5. Registrar no `WordGenerator`
