---
name: engenheiro-economico
description: Modela, calcula e defende a viabilidade financeira, valoração e eficiência ágil de projetos de software usando Engenharia Econômica. Use sempre que o usuário pedir análise de viabilidade de software, Fluxo de Caixa (CapEx/OpEx), VPL, TIR, Payback simples ou descontado, TMA, precificação de sistemas (Markup, SaaS, licenciamento, CAC/LTV, ponto de equilíbrio), Gerenciamento de Valor Agregado ágil (GVA/EVM com Story Points, VPA, VAG, CR, IDC, IDP, EAC), análise de substituição de sistemas legados, priorização econômica de backlog (Valor vs. Esforço) ou propostas econômicas de TI.
---

# Engenharia Econômica Aplicada a Projetos de Software

Skill especializada para transformar dados técnicos e de produto em modelagem financeira auditável, valoração de sistemas e propostas executivas de software.

## Princípio de Operação e Divulgação Progressiva

1. **Nunca estime cálculos financeiros de cabeça:** Delegue obrigatoriamente projeções de Fluxo de Caixa, VPL, TIR, Payback, Ponto de Equilíbrio, CAC/LTV, GVA e Priorização aos scripts determinísticos em `scripts/`.
2. **Carregue referências apenas sob demanda:**
   - Leia `references/formulas.md` quando precisar validar convenções matemáticas de equivalência financeira (VP/VF/TMA), depreciação ou decisão de substituição de legado.
   - Leia `references/aliquotas.md` quando o projeto envolver tributação brasileira (Simples Nacional Anexos III/V, Fator R, ISS, PIS/COFINS, IRPJ/CSLL) ou encargos trabalhistas (CLT vs. PJ).
3. **Padronize entregas executivas:** Utilize `assets/proposta_executiva_template.md` sempre que o objetivo for gerar uma proposta comercial/executiva ou relatório completo de valoração.

## Fluxo de Trabalho (12 Módulos da Disciplina)

### Etapa 1: Enquadramento Decisório e Trade-offs (Aulas 1 e 2)

- Identifique o contexto da decisão: novo produto (MVP/POC), evolução de plataforma, contratação sob encomenda (*Work for Hire*) ou substituição de sistema legado.
- Explicite as restrições orçamentárias, o custo de oportunidade e as alternativas comparadas (incluindo o cenário base de "não fazer nada").

### Etapa 2: Estruturação de Custos, Preço e Valor em TI (Aula 4)

- Separe rigorosamente **CapEx** (investimento inicial: desenvolvimento do MVP, setup, licenças perpétuas, equipamentos) de **OpEx** (custos operacionais recorrentes: nuvem, APIs, suporte, manutenção evolutiva/corretiva, impostos sobre faturamento).
- Classifique **Custos Diretos** (horas da equipe técnica, encargos) e **Custos Indiretos** (rateio administrativo, ferramentas, infraestrutura compartilhada).
- Inclua os custos invisíveis ("efeito iceberg"): QA/testes automatizados, *code review*, pipelines de CI/CD, *deploy* e estabilização pós-lançamento.
- Modele a estratégia de receita (SaaS recorrente, licença de uso, *Work for Hire* ou híbrido), comparando precificação baseada em custo (**Markup**) com **Valor Percebido** pelo cliente.

### Etapa 3: Fluxo de Caixa, Equivalência Financeira e Tributação (Aulas 3, 5, 6 e 8)

- Adote a convenção de **fim de período** (meses ou anos), alocando o investimento inicial no Período 0 (`FC0`).
- Desconsidere entradas de financiamento/dívidas na análise econômica pura para isolar o mérito intrínseco do projeto de software.
- Considere o **Valor Residual (VR)** e o retorno do capital de giro no último período do horizonte de análise, além da depreciação de ativos de TI (5 anos / 20% a.a.) e alíquotas aplicáveis (`references/aliquotas.md`).
- Defina a **Taxa Mínima de Atratividade (TMA)** compatível com o risco tecnológico e o custo de oportunidade do capital.

### Etapa 4: Cálculo Determinístico de Viabilidade e Valuation (Aulas 6 e 8)

Execute o script `scripts/calc_vpl_tir.py` passando os parâmetros do projeto em JSON:

```bash
python3 scripts/calc_vpl_tir.py --json '<PAYLOAD_JSON>'
```

Considere inflação (taxa aparente vs. taxa real pela equação de Fisher), depreciação de ativos/intangíveis e tributação (IRPJ/CSLL, ISS/PIS/COFINS) consultando `references/avaliacao_e_tributacao.md` quando o cenário exigir fluxo de caixa líquido de impostos.

### Etapa 4: Estruturação de Propostas e Precificação (Aula 7)

Para elaboração de propostas comerciais, orçamentos ou modelagem SaaS, leia `references/propostas_e_precificacao.md` e utilize o template estruturado em `assets/template_proposta_economica.md`.

Garanta a presença de: Resumo Executivo, Escopo (in/out), Premissas, Cronograma/Marcos, Tabela CAPEX/OPEX, BDI/Impostos, Ponto de Equilíbrio e indicadores comerciais (Margem de Contribuição, CAC/LTV quando aplicável).

### Etapa 5: Eficiência Ágil via GVA e Priorização Econômica (Aulas 9 e 12)

Quando houver dados de execução ágil (Sprints, Story Points planejados/entregues e custo real) ou backlog de funcionalidades para priorizar, leia `references/gva_e_priorizacao.md` e execute:

```bash
python3 scripts/calc_gva.py --json '<PAYLOAD_JSON>'
```

No GVA Ágil, calcule o Valor do Story Point (VSP = CTE / Total_SP_Planejado), VPA, VAG, CR, variações (VC, VP), índices (IDC, IDP) e estimativa no término (EAC), classificando a saúde do projeto nas faixas de desempenho.

Na Priorização Econômica, aplique WSJF (Custo de Atraso / Duração ou Esforço), ROI incremental por funcionalidade, Matriz Valor vs. Esforço ou Weighted Scoring Model.

### Etapa 6: Decisões Estratégicas, Sensibilidade e Ambientes Friccionais (Aulas 10 e 11)

Para decisões estruturais de longo prazo ou sob restrições severas, consulte `references/estrategia_e_friccoes.md`:

**Fazer ou Comprar (Make-or-Buy):** Compare o Custo Total de Propriedade (TCO) e o VPL/CAUE do desenvolvimento interno contra licenciamento/SaaS de terceiros, incluindo custos de integração e lock-in.

**Substituição de Sistemas Legados:** Avalie a vida econômica útil, custos crescentes de manutenção do sistema atual (Defensor) versus investimento e ganho operacional do novo sistema (Desafiante).

**Análise de Sensibilidade e Cenários:** Teste a variação de variáveis críticas (TMA, receita, atraso no cronograma, custo de nuvem) nos cenários Otimista, Base e Pessimista, identificando o ponto de equilíbrio (breakeven) da decisão.

**Ambientes Friccionais e Princípio "Bom o Suficiente" (Good Enough):** Avalie atritos reais (restrição de orçamento, alto custo de capital, assimetria de informação, urgência de time-to-market) para recomendar o nível ótimo de qualidade/arquitetura sem over-engineering, tratando o débito técnico como uma decisão financeira consciente (juros de manutenção futura vs. antecipação de receita).

## Padrão de Saída (Output Format)

Ao entregar análises econômico-financeiras ou recomendações técnicas, estruture a resposta de forma auditável:

**Enquadramento e Premissas:** Alternativas avaliadas (incluindo Status Quo), horizonte, TMA e premissas fiscais/operacionais adotadas.

**Tabela de Fluxo de Caixa / Métricas:** Apresentação tabular limpa período a período ou por funcionalidade/sprint.

**Indicadores Calculados (via Script):** VPL, TIR, Payback Simples/Descontado, IL, CAUE ou IDC/IDP/WSJF com interpretação objetiva.

**Análise de Risco e Sensibilidade:** Pontos críticos de atenção e impacto de variações nas premissas.

**Parecer Executivo:** Recomendação clara (Aprovar, Rejeitar, Postergar ou Priorizar) fundamentada nos critérios econômicos.

## Armadilhas Comuns (Gotchas)

**Custos Irreversíveis (Sunk Costs):** Valores já gastos antes da tomada de decisão (ex.: licenças já pagas ou protótipos anteriores) nunca devem entrar no cálculo de VPL das alternativas futuras.

**Descasa-mento de Taxa e Período:** Nunca desconte fluxos mensais usando uma TMA anual sem antes convertê-la de forma equivalente (i_mensal = (1 + i_anual)^(1/12) - 1).

**Inflação e Equação de Fisher:** Não misture fluxos de caixa em moeda constante (sem inflação) com TMA nominal/aparente (que embute inflação). Use sempre fluxos nominais com taxa aparente ou fluxos reais com taxa real.

**Fluxos Não Convencionais na TIR:** Projetos de software com grandes reinvestimentos futuros (ex.: migração de versão no ano 3) podem ter múltiplas inversões de sinal e gerar múltiplas TIRs ou TIR inexistente; nesses casos, priorize sempre o VPL como critério soberano de decisão.

**Formatação Monetária vs. Matemática:** Evite misturar o cifrão R$ dentro de blocos matemáticos delimitadores para não quebrar a renderização do Markdown.