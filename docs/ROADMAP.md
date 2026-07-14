# Roadmap - GDANT

## Visão Geral

Roadmap detalhado do GDANT até a versão 1.0.0 (Release Estável).

## Sprints Planejadas

### Sprint 5 - Extractors e Parser (Próxima)
- Implementar módulo de Extractors especializados
- Criar Parser que assembla ProcessData
- Implementar testes unitários
- Validar extração com PDFs de exemplo

### Sprint 6 - WordGenerator
- Implementar WordGenerator para preencher template
- Suportar placeholders dinâmicos
- Validar formatação de documentos

### Sprint 7 - PdfGenerator
- Implementar PdfGenerator
- Integrar com Word (python-docx)
- Testes de geração de PDFs

### Sprint 8 - Engine e Orquestração
- Implementar classe Engine
- Orquestrar fluxo completo: PDF → ProcessData → Documento
- Testes de integração

### Sprint 9 - Interface PyQt6
- Implementar interface gráfica
- QListWidget para seleção de PDFs
- Visualização de resultados
- Menu e configurações

### Sprint 10 - Refinamento e Testes
- Testes completos de usabilidade
- Documentação final
- Correção de bugs
- Performance tuning

## Milestones até v1.0.0

| Sprint | Versão | Milestone |
|--------|--------|--------|
| 4-5 | 0.2.0 | Parser funcional |
| 6-7 | 0.5.0 | Geração de documentos |
| 8-9 | 0.8.0 | Interface completa |
| 10 | 1.0.0 | Release estável |

## Pós-v1.0.0 (Melhorias Futuras)

- Suporte a múltiplos tipos de processos
- Integração com sistemas legados
- Exportação em múltiplos formatos
- Histórico de processamentos
- Validação automática de dados
