# SETUP - Instalação do GDANT

## Requisitos do Sistema

- **Python**: 3.9+
- **Sistema Operacional**: Windows 10/11, macOS, Linux
- **Espaço em disco**: ~500MB (dependências + modelos OCR)

---

## Instalação Passo a Passo

### 1. Clonar Repositório

```bash
git clone https://github.com/sirtuca/GDANT.git
cd GDANT
```

### 2. Criar Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Instalação de Dependências Específicas

### PaddleOCR

PaddleOCR fornece reconhecimento ótico de caracteres para páginas scaneadas.

```bash
pip install paddleocr
```

**Nota:** Primeira execução baixará ~200MB de modelos treinados. Pode levar 2-5 minutos.

### pdf2image

pdf2image converte páginas PDF em imagens para processamento OCR.

```bash
pip install pdf2image
```

**Requer Poppler instalado no seu sistema (veja abaixo).**

### Poppler

Poppler é uma biblioteca para renderização de PDFs. Necessária para pdf2image funcionar.

#### Windows

**Opção A: Usando Chocolatey (Recomendado)**

```bash
choco install poppler
```

**Opção B: Download Manual**

1. Baixar: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extrair para diretório, exemplo: `C:\poppler`
3. Adicionar ao PATH do Windows:
   - Painel de Controle → Sistema → Variáveis de Ambiente
   - Editar variável `Path`
   - Adicionar: `C:\poppler\Library\bin`
   - Reiniciar terminal/IDE

#### macOS

```bash
brew install poppler
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-get install poppler-utils
```

---

## Verificar Instalação

### Verificar Python

```bash
python --version
# Esperado: Python 3.9 ou superior
```

### Verificar Poppler

```bash
pdftotext --version
# Se retorna erro, Poppler não está instalado ou não está no PATH
```

### Verificar PaddleOCR

```bash
python -c "from paddleocr import PaddleOCR; print('PaddleOCR OK')"
# Se retorna erro, execute: pip install paddleocr
```

### Verificar pdf2image

```bash
python -c "from pdf2image import convert_from_path; print('pdf2image OK')"
# Se retorna erro, execute: pip install pdf2image
```

---

## Troubleshooting

### "pdftotext command not found" ou "poppler not found"

**Problema:** Poppler não está instalado ou não está no PATH.

**Solução:**

1. Verificar se instalou:
   ```bash
   pdftotext --version
   ```

2. Se não funciona:
   - **Windows**: Reinstalar com `choco install poppler` ou adicionar manualmente ao PATH
   - **macOS**: `brew install poppler`
   - **Linux**: `sudo apt-get install poppler-utils`

3. Após instalar, **reiniciar terminal/IDE** para recarregar PATH

### "ModuleNotFoundError: No module named 'paddleocr'"

**Solução:**
```bash
pip install paddleocr
```

### "ModuleNotFoundError: No module named 'pdf2image'"

**Solução:**
```bash
pip install pdf2image
```

### OCR muito lento na primeira execução

**Esperado:** PaddleOCR baixa modelos (~200MB) na primeira execução. Pode levar vários minutos. Isso ocorre apenas uma vez.

---

## requirements.txt

Arquivo esperado na raiz do projeto:

```
pdfplumber>=1.0.0
python-docx>=0.8.11
paddleocr>=2.7.0
pdf2image>=1.16.3
Pillow>=10.0.0
```

Se `requirements.txt` não existir:

```bash
pip install pdfplumber python-docx paddleocr pdf2image Pillow
```

---

**Instalação concluída!** Você está pronto para usar GDANT.
