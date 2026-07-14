# Guia de Extractors - GDANT

## Filosofia dos Extractors

Os Extractors são o coração da extração de dados no GDANT. Cada extractor tem uma filosofia clara e bem definida:

### Princípios Fundamentais

1. **Uma Responsabilidade:** Cada extractor extrai um tipo específico de informação
2. **Sem Regras de Negócio:** Extractors não implementam regras complexas
3. **Reutilizáveis:** Podem ser usados em diferentes contextos
4. **Testáveis:** Cada extractor é testável isoladamente
5. **Simples:** Código limpo e direto

## Padrão de Desenvolvimento

### Estrutura de um Extractor

```python
class ExtractorNome:
    """
    Extrai dados específicos do texto bruto.
    
    Responsabilidade: Extrair um tipo único de informação.
    Não contém lógica de negócio complexa.
    """
    
    def extract(self, text: str) -> str | None:
        """
        Extrai informação do texto.
        
        Args:
            text: Texto bruto extraído do PDF
        
        Returns:
            Valor extraído ou None se não encontrado
        """
        # 1. Buscar padrões em patterns.py
        # 2. Validar formato básico
        # 3. Limpar/formatar valor
        # 4. Retornar valor tipado
        pass
```

### Fluxo de Extração

```
Texto Bruto
    ↓
[Busca Padrões] → patterns.py
    ↓
[Extrai Valor]
    ↓
[Valida Formato]
    ↓
[Limpa Valor]
    ↓
Valor Tipado
```

## Extractors Básicos

### ExtractorCpf

**Objetivo:** Extrair CPF do texto

**Entrada:** Texto bruto  
**Saída:** String com CPF (ou None)

**Lógica:**
1. Buscar padrões de CPF em `patterns.CPF_PATTERNS`
2. Validar formato (11 dígitos)
3. Limpar formatação
4. Retornar CPF formatado ou None

**Exemplo:**
```python
extractor = ExtractorCpf()
resultado = extractor.extract("CPF do contribuinte: 123.456.789-00")
# Retorna: "12345678900" ou "123.456.789-00"
```

### ExtractorCnpj

**Objetivo:** Extrair CNPJ do texto

**Entrada:** Texto bruto  
**Saída:** String com CNPJ (ou None)

**Lógica:**
1. Buscar padrões de CNPJ em `patterns.CNPJ_PATTERNS`
2. Validar formato (14 dígitos)
3. Limpar formatação
4. Retornar CNPJ formatado ou None

### ExtractorEmail

**Objetivo:** Extrair email do texto

**Entrada:** Texto bruto  
**Saída:** String com email (ou None)

**Lógica:**
1. Buscar padrões de email em `patterns.EMAIL_PATTERNS`
2. Validar formato básico (contém @)
3. Limpar espaços
4. Retornar email em minúsculas ou None

### ExtractorPhone

**Objetivo:** Extrair telefone do texto

**Entrada:** Texto bruto  
**Saída:** String com telefone (ou None)

**Lógica:**
1. Buscar padrões de telefone em `patterns.PHONE_PATTERNS`
2. Extrair números
3. Validar quantidade de dígitos
4. Retornar telefone formatado ou None

### ExtractorProcessNumber

**Objetivo:** Extrair número do processo do texto

**Entrada:** Texto bruto  
**Saída:** String com número do processo (ou None)

**Lógica:**
1. Buscar padrões em `patterns.PROCESS_NUMBER_PATTERNS`
2. Extrair sequência numérica
3. Validar comprimento
4. Retornar número formatado ou None

## Padrão de Desenvolvimento

### Passo 1: Identificar o Tipo de Dado

Qual tipo de informação será extraída?
- CPF, Email, Telefone, etc?

### Passo 2: Registrar Padrões

Adicionar padrões textuais em `patterns.py`:

```python
SEU_TIPO_PATTERNS = [
    "padrão 1",
    "padrão 2",
    "padrão 3",
]
```

### Passo 3: Implementar Extractor

Criar classe que implementa a extração:

```python
from patterns import SEU_TIPO_PATTERNS

class ExtractorSeuTipo:
    def extract(self, text: str) -> str | None:
        # Implementar lógica
        pass
```

### Passo 4: Escrever Testes

Testes unitários para validar:

```python
def test_extract_valid():
    extractor = ExtractorSeuTipo()
    result = extractor.extract("Seu tipo: valor")
    assert result == "valor esperado"

def test_extract_not_found():
    extractor = ExtractorSeuTipo()
    result = extractor.extract("Texto sem o dado")
    assert result is None
```

### Passo 5: Integrar ao Parser

Adicionar ao Parser:

```python
from extractors import ExtractorSeuTipo

class Parser:
    def parse(self, text: str) -> ProcessData:
        extractor = ExtractorSeuTipo()
        seu_tipo = extractor.extract(text)
        # ...
```

## Regras Importantes

### ✅ Faça

- ✅ Uma responsabilidade por extractor
- ✅ Retornar None se não encontrar
- ✅ Limpar e validar valores
- ✅ Usar patterns.py para padrões
- ✅ Implementar testes
- ✅ Documentar com docstrings
- ✅ Ser determinístico

### ❌ Não Faça

- ❌ Múltiplas responsabilidades
- ❌ Chamar outros extractors
- ❌ Implementar regras de negócio
- ❌ Hardcodificar padrões
- ❌ Deixar sem testes
- ❌ Ser não-determinístico (aleatório)
- ❌ Modificar o texto de entrada

## Exemplo Completo

```python
# patterns.py
CPF_PATTERNS = [
    "cpf",
    "c.p.f.",
    "cpf do contribuinte",
]

# extractors.py
import re
from patterns import CPF_PATTERNS

class ExtractorCpf:
    """Extrai CPF do texto bruto."""
    
    def extract(self, text: str) -> str | None:
        """
        Extrai CPF do texto.
        
        Busca por padrões conhecidos e valida formato.
        """
        # Buscar padrão
        for pattern in CPF_PATTERNS:
            # Lógica de busca
            match = re.search(rf"{pattern}[:\s]*(\d{{3}}\.?\d{{3}}\.?\d{{3}}-?\d{{2}})", text, re.IGNORECASE)
            if match:
                cpf = match.group(1)
                # Limpar formatação
                cpf_limpo = re.sub(r"\D", "", cpf)
                # Validar
                if len(cpf_limpo) == 11:
                    return cpf_limpo
        
        return None

# tests.py
from extractors import ExtractorCpf

def test_extract_cpf():
    extractor = ExtractorCpf()
    
    # Teste com padrão válido
    text = "CPF do contribuinte: 123.456.789-00"
    result = extractor.extract(text)
    assert result == "12345678900"
    
    # Teste sem dados
    text = "Nenhum CPF aqui"
    result = extractor.extract(text)
    assert result is None
```
