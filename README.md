# GDANT - Gerador de Dívida Ativa

## Descrição

GDANT é uma aplicação Python que recebe uma pasta contendo Processos Administrativos em PDF e gera Termos de Inscrição em Dívida Ativa em DOCX e PDF.

## Requisitos

- Python 3.12+
- PySide6

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
python src/main.py
```

## Estrutura do Projeto

```
GDANT/
├── src/
│   ├── main.py
│   ├── interface.py
│   ├── config.py
│   └── processor.py
├── config/
│   └── config.json
├── templates/
├── manuals/
├── input/
├── output/
└── requirements.txt
```

## Funcionalidades

- Interface gráfica intuitiva com PySide6
- Configuração flexível de templates e manuais
- Suporte a geração de arquivos DOCX e PDF
- Lembrança automática das últimas configurações utilizadas
- Barra de progresso e área de status
