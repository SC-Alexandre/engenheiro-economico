# Proposta Econômica e Relatório de Valoração de Software

## 1. Sumário Executivo e Contexto Decisório
- **Sistema / Projeto:** [Nome do Sistema]
- **Problema de Negócio & Solução:** [Resumo objetivo]
- **Enquadramento (Aulas 1 e 2):** [MVP / Evolução / Substituição de Legado]
- **Veredito Econômico:** [Viável / Inviável — destaque de VPL, TIR e Payback]

## 2. Escopo, Premissas e Propriedade Intelectual
- **Dentro do Escopo:** [Módulos e entregas]
- **Fora do Escopo:** [Limitações explícitas]
- **Premissas Técnicas e Financeiras:** [Horizonte de análise, TMA, regime tributário, premissas de adoção]
- **Titularidade de Propriedade Intelectual (PI):** [Obra por Encomenda / *Work for Hire* vs. Licenciamento SaaS]

## 3. Estrutura de Custos (CapEx vs. OpEx) e Custos Invisíveis
| Categoria | Tipo | Classificação | Descrição | Valor Estimado (R$) |
| :--- | :--- | :--- | :--- | ---: |
| Desenvolvimento Inicial | CapEx | Direto | Horas de engenharia, arquitetura e UI/UX | 0,00 |
| Qualidade e Entrega ("Iceberg") | CapEx | Direto | Testes automatizados, QA, *code review*, CI/CD | 0,00 |
| Infraestrutura Cloud & APIs | OpEx | Indireto | Hospedagem, banco de dados, observabilidade | 0,00/mês |
| Manutenção e Suporte | OpEx | Direto | Correção de bugs e sustentação operacional | 0,00/mês |

## 4. Fluxo de Caixa Projetado e Indicadores de Viabilidade
[Inserir tabela completa gerada por `scripts/calc_vpl_tir.py`]
- **VPL (Valor Presente Líquido):** R$ [valor]
- **TIR (Taxa Interna de Retorno):** [valor]% ao período (vs. TMA de [valor]%)
- **Payback Simples / Descontado:** [valor] / [valor] períodos

## 5. Eficiência Ágil (GVA / EVM) e Priorização de Backlog
[Inserir métricas calculadas por `scripts/calc_gva.py`: VPA, VAG, CR, IDC, IDP, EAC e tabela de priorização Valor vs. Esforço]

## 6. Modelo de Negócio, Precificação e Matriz de Riscos
- **Modelo de Monetização:** [SaaS B2B/B2C, Licenciamento, *Work for Hire*]
- **Unit Economics:** Ticket Médio, Margem de Contribuição, Ponto de Equilíbrio, CAC e LTV
- **Riscos e Mitigações:** [Riscos técnicos, de adoção e financeiros com planos de resposta]