# EXTRACTION MAP

## Introdução

Este documento mapeia **todos os campos necessários** para gerar o Termo de Inscrição em Dívida Ativa do GDANT.

Conecta:

- **Manual Técnico** - Definição e regras de cada campo
- **Template Mestre** - Placeholders do documento Word
- **Processo Administrativo PDF** - Fonte de dados bruta
- **Extractors** - Funções que extraem informações específicas
- **ProcessData** - Estrutura contratual de dados
- **WordFields** - Campos finais do template Word

Este é o **mapa oficial** que orienta o desenvolvimento de novos extractors e expansão do ProcessData.

---

## Fontes de Dados

As informações do Termo vêm de documentos específicos dentro do Processo Administrativo:

### Auto de Infração

Fonte para:
- Nome do contribuinte
- CPF/CNPJ
- Inscrição Econômica (IE)
- Telefone
- Endereço completo (logradouro, número, complemento, bairro, município, UF, CEP)
- Origem da dívida (código da infração)
- Fundamento legal

### DILT Dispatch

Fonte para:
- COD (Código da Dívida)
- Natureza da dívida
- Modalidade de lançamento
- Valor da dívida
- Data do vencimento

### AR, E-mail, WhatsApp ou Edital

Fonte para:
- Prazo administrativo
- Data de decurso de prazo

### Auto de Infração

Fonte para:
- Número da Infração
- Data da Infração
- Lei específica
- Data da Lei
- Artigo
- Inciso
- Parágrafo
- Alínea
- Item

---

## Mapa de Campos

| Campo Template | Campo ProcessData | Documento Fonte | Estratégia Extração | Extractor | Obrigatório? | Status |
|---|---|---|---|---|---|---|
| T | year | Manual | Extraído da data do documento | `extract_year` | Sim | ⏳ Planejado |
| ANO | year | Manual | Extraído da data do documento | `extract_year` | Sim | ⏳ Planejado |
| DT | current_date | Manual | Data de emissão | `extract_current_date` | Sim | ⏳ Planejado |
| NOME | taxpayer_name | Auto de Infração | Regex no cabeçalho | `extract_taxpayer_name` | Sim | ⏳ Planejado |
| DOC | cpf_cnpj | Auto de Infração | Regex (CPF ou CNPJ) | `extract_cpf_cnpj` | Sim | ✅ Implementado |
| IE | inscricao_economica | Auto de Infração | Regex após "IE" ou "Inscrição" | `extract_inscricao_economica` | Não | ⏳ Planejado |
| LOG | street_address | Auto de Infração | Regex após "Endereço" | `extract_address` | Sim | ⏳ Planejado |
| NR | address_number | Auto de Infração | Regex de número após rua | `extract_address_number` | Sim | ⏳ Planejado |
| COMP | address_complement | Auto de Infração | Regex entre endereço e bairro | `extract_address_complement` | Não | ⏳ Planejado |
| BAIRRO | neighborhood | Auto de Infração | Regex após "Bairro" | `extract_neighborhood` | Não | ⏳ Planejado |
| MUN | city | Auto de Infração | Regex após "Município" | `extract_city` | Sim | ⏳ Planejado |
| UF | state | Auto de Infração | Regex 2 letras após "UF" ou estado | `extract_state` | Sim | ⏳ Planejado |
| CEP | zip_code | Auto de Infração | Regex padrão CEP (XXXXX-XXX) | `extract_zip_code` | Não | ⏳ Planejado |
| FONE | phone | Auto de Infração | Regex telefone com DDD | `extract_phone` | Não | ⏳ Planejado |
| EMAIL | email | Auto de Infração | Regex padrão email | `extract_email` | Não | ⏳ Planejado |
| APP | whatsapp | Auto de Infração | Se telefone, usar mesmo (padrão Brasil) | `extract_whatsapp` | Não | ⏳ Planejado |
| LOGC | legal_address_street | Auto de Infração | Se diferente, usar mesmo que LOG | `extract_legal_address` | Não | ⏳ Planejado |
| NRC | legal_address_number | Auto de Infração | Se diferentes, usar mesmo que NR | `extract_legal_address_number` | Não | ⏳ Planejado |
| COMPC | legal_address_complement | Auto de Infração | Se diferente, usar mesmo | `extract_legal_address_complement` | Não | ⏳ Planejado |
| BAIRROC | legal_neighborhood | Auto de Infração | Se diferente, usar mesmo | `extract_legal_neighborhood` | Não | ⏳ Planejado |
| MUNC | legal_city | Auto de Infração | Se diferente, usar mesmo | `extract_legal_city` | Não | ⏳ Planejado |
| UFC | legal_state | Auto de Infração | Se diferente, usar mesmo | `extract_legal_state` | Não | ⏳ Planejado |
| CEPC | legal_zip_code | Auto de Infração | Se diferente, usar mesmo | `extract_legal_zip_code` | Não | ⏳ Planejado |
| ORIGEM | origin_debt | Auto de Infração | Identificação de origem (infração, omissão, etc) | `extract_origin_debt` | Sim | ⏳ Planejado |
| COD | debt_code | DILT Dispatch | Regex código da dívida | `extract_cod` | Sim | ⏳ Planejado |
| NAT | debt_nature | DILT Dispatch | Descrição natureza | `extract_debt_nature` | Sim | ⏳ Planejado |
| MOD | debt_modality | DILT Dispatch | Modalidade de lançamento | `extract_debt_modality` | Sim | ⏳ Planejado |
| PROC | process_number | Auto de Infração / Header | Regex padrão SEI (XXXXXX/YYYY-ZZ) | `extract_process_number` | Sim | ✅ Implementado |
| AI | infraction_number | Auto de Infração | Regex padrão IA (XXXXX/YY) | `extract_infraction_number` | Sim | ✅ Implementado |
| DTAI | infraction_date | Auto de Infração | Regex data após "Data" | `extract_infraction_date` | Sim | ⏳ Planejado |
| ANOL | year_infraction | Auto de Infração | Extraído de DTAI | `extract_year_infraction` | Sim | ⏳ Planejado |
| VALOR | debt_amount | DILT Dispatch | Regex valores monetários | `extract_debt_amount` | Sim | ⏳ Planejado |
| DECURSO | administrative_deadline | AR/Email/Edital | Data de decurso ou AR | `extract_administrative_deadline` | Sim | ⏳ Planejado |
| VENC | due_date | DILT Dispatch | Data de vencimento | `extract_due_date` | Sim | ⏳ Planejado |
| F_TPLEI | legal_basis_type | Auto de Infração | Tipo de lei (Estadual, Federal, etc) | `extract_legal_basis_type` | Sim | ⏳ Planejado |
| F_LEI | legal_basis_number | Auto de Infração | Número da lei | `extract_legal_basis_number` | Sim | ⏳ Planejado |
| F_DTLEI | legal_basis_date | Auto de Infração | Data de publicação da lei | `extract_legal_basis_date` | Não | ⏳ Planejado |
| F_ART | legal_article | Auto de Infração | Artigo da lei | `extract_legal_article` | Sim | ⏳ Planejado |
| F_INC | legal_inciso | Auto de Infração | Inciso do artigo | `extract_legal_inciso` | Não | ⏳ Planejado |
| F_PAR | legal_paragraph | Auto de Infração | Parágrafo do artigo | `extract_legal_paragraph` | Não | ⏳ Planejado |
| F_ALIN | legal_aliquota | Auto de Infração | Alínea do artigo | `extract_legal_aliquota` | Não | ⏳ Planejado |
| F_ITEM | legal_item | Auto de Infração | Item do artigo | `extract_legal_item` | Não | ⏳ Planejado |
| LOCAL_DATA | location_and_date | Manual | Cidade e data de emissão | `extract_location_and_date` | Sim | ⏳ Planejado |

---

## Categorias de Campos

### Campos Fixos

Valores que NÃO variam entre processos:
- `year` - Extraído da data
- `current_date` - Data de emissão
- `legal_basis_type` - Configurável globalmente

### Campos Extraídos

Extratos diretamente do Processo Administrativo:
- `taxpayer_name`, `cpf_cnpj`, `inscricao_economica`
- `street_address`, `address_number`, `neighborhood`, `city`, `state`, `zip_code`
- `phone`, `email`
- `infraction_number`, `infraction_date`
- `debt_code`, `debt_amount`, `due_date`
- `legal_article`, `legal_inciso`, `legal_paragraph`

### Campos Calculados

Derivados de outros campos:
- `year_infraction` - Extraído de `infraction_date`
- `legal_address_*` - Mesmo que endereço principal se não diferente
- `administrative_deadline` - Baseado em `due_date` + prazo

### Campos de Interpretação Legal

Requerem conhecimento de regras:
- `origin_debt` - Identificação do tipo de infração
- `debt_nature` - Classificação da dívida
- `debt_modality` - Tipo de lançamento

### Campos Apenas do Template

Aparecem no Word mas não precisam extração:
- `LOCAL_DATA` - Preenchido durante geração

---

## Status da Implementação Atual

### Extractors Implementados

✅ **extract_process_number()** - Extrai número SEI  
✅ **extract_infraction_number()** - Extrai número IA  
✅ **extract_cpf_cnpj()** - Extrai CPF ou CNPJ  

### ProcessData Preenchido Pelo Parser

✅ `source_pdf` - Caminho do arquivo  
✅ `raw_text` - Texto bruto do PDF  
✅ `process_number` - Número do processo  
✅ `infraction_number` - Número da infração  
✅ `cpf_cnpj` - CPF ou CNPJ do contribuinte  

### Campos Não Preenchidos

⏳ Todos os outros campos listados na tabela acima

---

## Próximos Extractors Recomendados

### Prioridade Alta

1. **extract_taxpayer_name()** - Nome do contribuinte (obrigatório)
2. **extract_address()** - Endereço completo
3. **extract_city()** - Município
4. **extract_state()** - Estado (UF)
5. **extract_debt_amount()** - Valor da dívida (obrigatório)
6. **extract_cod()** - Código da dívida
7. **extract_due_date()** - Data de vencimento
8. **extract_infraction_date()** - Data da infração

### Prioridade Média

9. **extract_inscricao_economica()** - Inscrição econômica
10. **extract_phone()** - Telefone
11. **extract_email()** - Email
12. **extract_zip_code()** - CEP
13. **extract_legal_basis_number()** - Número da lei
14. **extract_legal_article()** - Artigo

### Prioridade Baixa

15. **extract_origin_debt()** - Origem da dívida
16. **extract_legal_inciso()** - Inciso
17. **extract_legal_paragraph()** - Parágrafo
18. **extract_neighborhood()** - Bairro
19. **extract_address_complement()** - Complemento

---

## Regra Arquitetônica Importante

### ProcessData Não é o Destino Final

**ProcessData é o contrato ATUAL** entre Parser e WordGenerator.

Mas **nem todos os campos precisam estar em ProcessData**.

### Evolução Futura Esperada

A arquitetura pode evoluir para separar:

```
RawProcessData
├─ Dados brutos extratos (como estão hoje)
├─ process_number
├─ infraction_number
├─ cpf_cnpj
└─ ...

LegalProcessData
├─ Dados interpretados (com regras)
├─ origin_debt (identificado)
├─ debt_classification
├─ legal_basis (analisado)
└─ ...

WordFields
├─ Dados prontos para template
├─ formatted_cpf_cnpj
├─ formatted_amount
├─ formatted_date
└─ ...
```

### Por Enquanto

ProcessData permanece como **estrutura única de dados** entre Parser e WordGenerator.

Quando essa separação for necessária, serão criadas novas estruturas mantendo os extractors independentes.

---

## Próximos Passos

1. Implementar extractors para campos de **prioridade alta**
2. Estender ProcessData conforme novos campos são extratos
3. Atualizar Parser para coordenar novos extractors
4. Conforme ProcessData crescer, revisitar arquitetura de separação
5. Eventualmente implementar LegalProcessData se necessário

**Este mapa é vivo.** Será atualizado conforme novos extractors forem implementados.

---

**Data de Atualização:** 2026-07-01  
**Status:** Sprint 6 Completa - Documentação de Roadmap de Extração
