---
name: engenheiro-economico
description: 'Modela, calcula e avalia a viabilidade financeira, valoração e eficiência ágil de projetos de software usando Engenharia Econômica. Utilize quando o usuário solicitar análise de fluxo de caixa (CapEx/OpEx), VPL, TIR, Payback, TMA, precificação de software, modelos SaaS, CAC/LTV, ponto de equilíbrio, Gerenciamento de Valor Agregado (GVA/EVM), priorização econômica de backlog, substituição de sistemas legados ou propostas econômicas de TI.'
---

# Engenharia Econômica Aplicada a Projetos de Software

Skill especializada para transformar dados técnicos e de produto em modelagem financeira auditável, valoração de sistemas e propostas executivas de software.

## Princípio de Operação e Divulgação Progressiva

1. **Nunca estime cálculos financeiros de cabeça:** Delegue obrigatoriamente projeções de Fluxo de Caixa, VPL, TIR, Payback, Ponto de Equilíbrio, CAC/LTV, GVA e Priorização aos scripts determinísticos em `scripts/`.
2. **Carregue referências apenas sob demanda:**
   - Leia `references/formulas.md` quando precisar consultar fórmulas de equivalência financeira (VP/VF/TMA), VPL, TIR, Payback, indicadores SaaS, GVA/EVM, priorização econômica, CAUE, análise de substituição de sistemas e demais fundamentos matemáticos.
   - Leia `references/aliquotas.md` quando o projeto envolver tributação brasileira (Simples Nacional, Anexos III/V, Fator R, ISS, PIS/COFINS, IRPJ/CSLL) ou encargos trabalhistas (CLT vs. PJ).
3. **Padronize entregas executivas:** Utilize `assets/proposta_executiva_template.md` sempre que o objetivo for gerar uma proposta comercial/executiva ou relatório completo de valoração.


## Fluxo de Trabalho

A análise deve seguir as etapas abaixo, selecionando os módulos pertinentes ao contexto do projeto. Nem todas as análises exigem a execução de todos os módulos.

### Etapa 1: Enquadramento Decisório e Trade-offs

- Identifique o contexto da decisão: desenvolvimento de novo produto (MVP/POC), evolução de plataforma, contratação sob encomenda (Work for Hire) ou substituição de sistema legado.
- Identifique o problema de negócio, os objetivos do projeto e os benefícios esperados.
- Explicite as restrições orçamentárias, o custo de oportunidade e as alternativas disponíveis.
- Inclua o cenário base de não realizar o projeto (Status Quo), sempre que aplicável.
- Identifique as premissas técnicas, operacionais e financeiras necessárias à análise.

### Etapa 2: Estruturação de Custos, Preço e Valor em TI

- Separe rigorosamente CapEx (investimentos iniciais e ativos capitalizáveis) de OpEx (custos operacionais recorrentes).
- Classifique os custos em diretos (horas da equipe técnica, encargos e serviços diretamente relacionados) e indiretos (administração, ferramentas e infraestrutura compartilhada).
- Considere os custos invisíveis do desenvolvimento, incluindo QA, testes automatizados, code review, CI/CD, deploy e estabilização pós-lançamento.
- Identifique o modelo de receita: SaaS recorrente, licenciamento, Work for Hire ou modelo híbrido.
- Diferencie precificação baseada em custos (Markup) de precificação baseada no valor percebido pelo cliente.

### Etapa 3: Fluxo de Caixa, Equivalência Financeira e Tributação

- Defina o horizonte de análise, a periodicidade dos fluxos e a convenção de fim de período.
- Aloque o investimento inicial no Período 0 (FC0).
- Estruture as entradas e saídas de caixa, identificando receitas, custos operacionais, investimentos adicionais, impostos e capital de giro.
- Desconsidere entradas de financiamento e dívidas na análise econômica pura, isolando o mérito econômico do projeto.
- Considere o valor residual dos ativos e a recuperação do capital de giro no último período, quando aplicável.
- Defina a Taxa Mínima de Atratividade (TMA), considerando o custo de oportunidade e o risco do projeto.
- Consulte references/formulas.md para validar as fórmulas de equivalência financeira, VPL, TIR, Payback e depreciação.
- Consulte references/aliquotas.md quando houver necessidade de modelagem tributária brasileira ou encargos trabalhistas.
- Mantenha coerência entre a periodicidade dos fluxos e a taxa de desconto utilizada.
- Diferencie fluxos nominais e reais, aplicando a equação de Fisher quando necessário.
- O modelo tributário implementado no script é simplificado: aplica uma alíquota sobre a receita bruta. Não representa uma apuração fiscal completa e não contempla automaticamente todas as particularidades dos regimes tributários brasileiros. Identifique essa simplificação nos resultados e não apresente o cálculo como apuração oficial de tributos.

### Etapa 4: Cálculo Determinístico de Viabilidade e Valuation

Execute obrigatoriamente o script scripts/calc_vpl_tir.py para calcular os indicadores de viabilidade financeira.

Exemplo de execução:

python3 scripts/calc_vpl_tir.py --json '<PAYLOAD_JSON>'

O payload JSON deve conter os parâmetros exigidos pelo script, incluindo TMA, investimento inicial e fluxos financeiros projetados.

Analise os resultados:
- Fluxo de Caixa Líquido por período.
- Valor Presente Líquido (VPL).
- Taxa Interna de Retorno (TIR).
- Payback Simples e Descontado.
- Índice de Lucratividade (IL).
- Indicadores de Unit Economics, quando aplicáveis.

O Índice de Lucratividade (IL) implementado no script é a razão entre o
valor presente dos benefícios de caixa e o valor presente dos custos e
desembolsos do projeto. Os benefícios incluem receita bruta líquida dos
tributos simplificados, valor residual, recuperação do capital de giro e
outras entradas existentes no modelo. Os custos incluem CapEx inicial,
capital de giro inicial, OpEx e CapEx adicional. Desconte cada componente
pela TMA correspondente ao período, sem compensar benefícios e custos
antes da classificação e sem contabilizar componentes duas vezes. Se o
valor presente dos custos for zero, o IL é indefinido; se os benefícios
forem zero e os custos forem positivos, o IL é zero. Essa medida abrangente
benefício/custo é distinta da formulação tradicional baseada apenas no
investimento inicial; interprete-a junto ao VPL.

Interprete os indicadores considerando as premissas adotadas. Utilize o VPL como principal critério de decisão quando houver limitações na interpretação da TIR.

Não invente resultados: se faltarem dados, solicite as informações necessárias ou apresente cenários explicitamente identificados como estimativas.

### Etapa 5: Propostas Econômicas, Precificação e Modelo de Negócio

Quando o objetivo for elaborar uma proposta comercial, orçamento ou relatório executivo de valoração:

- Consulte references/formulas.md para as formulações de precificação e indicadores econômicos pertinentes.
- Utilize assets/proposta_executiva_template.md como estrutura de apresentação.
- Apresente resumo executivo, escopo, premissas e cronograma.
- Estruture a tabela de CapEx e OpEx.
- Apresente os tributos, encargos e demais custos considerados.
- Calcule o ponto de equilíbrio e a margem de contribuição, quando aplicáveis.
- Apresente CAC e LTV em modelos de negócio recorrentes, quando houver dados suficientes.
- Diferencie as premissas estimadas dos dados efetivamente informados.

### Etapa 6: Eficiência Ágil, Estratégia e Priorização Econômica

**Gerenciamento de Valor Agregado:**

Quando houver dados de execução ágil, como orçamento, Story Points planejados e entregues e custos realizados, consulte references/formulas.md e execute:

python3 scripts/calc_gva.py --json '<PAYLOAD_JSON>'

Calcule e interprete:
- Valor por Story Point (VSP).
- Valor Planejado (VPA).
- Valor Agregado (VAG).
- Custo Real (CR).
- Variação de Custo (VC).
- Variação de Prazo (VP).
- Índice de Desempenho de Custo (IDC).
- Índice de Desempenho de Prazo (IDP).
- Estimativa no Término (EAC).
- A conversão de Story Points em valores monetários é uma aproximação gerencial baseada na distribuição proporcional do orçamento pelos Story Points totais do projeto. Não representa necessariamente o valor econômico efetivamente produzido pelas funcionalidades entregues.

Explique as premissas da conversão de Story Points em valor monetário.

**Estratégia e Substituição de Sistemas:**

Quando houver decisões estruturais de longo prazo, consulte references/formulas.md para avaliar:

- Fazer ou Comprar (Make-or-Buy): compare o Custo Total de Propriedade (TCO) e os custos de desenvolvimento interno com licenciamento ou SaaS de terceiros.
- Substituição de Sistemas Legados: compare os custos futuros de manutenção do sistema atual com o investimento e os benefícios operacionais do novo sistema.
- Ambientes Friccionais e Good Enough: avalie restrições orçamentárias, urgência de entrega, custo de oportunidade e o equilíbrio entre qualidade, arquitetura e custos.
- Débito Técnico: avalie os custos futuros de manutenção em relação aos benefícios de antecipar a entrega de funcionalidades.

**Priorização Econômica de Backlog:**

Quando houver funcionalidades a priorizar, utilize o script scripts/calc_gva.py para aplicar a Matriz Valor vs. Esforço (Weighted Scoring Model).

- Avalie o valor de negócio, custo, esforço e risco.
- Utilize critérios e escalas coerentes, identificando se notas maiores representam condições mais favoráveis ou desfavoráveis.
- Apresente o ranking de prioridades e explique os critérios utilizados.
- Não atribua pontuações sem informações suficientes ou premissas explicitadas.
- O ranking produzido pelo script utiliza um índice comparativo de benefícios ponderados em relação aos sacrifícios ponderados (esforço e custo). Esse índice auxilia a comparação entre funcionalidades, mas não representa ROI ou rentabilidade financeira. As notas e os pesos devem ser justificados pelas informações disponíveis e pelas premissas adotadas.

## Padrão de Saída (Output Format)

Toda análise econômico-financeira deve apresentar resultados organizados, rastreáveis e fundamentados nos dados fornecidos pelo usuário.

Adapte a profundidade da resposta à complexidade da solicitação, sem omitir informações essenciais para a tomada de decisão.

### 1. Enquadramento e Premissas

Apresente:
- Identificação do sistema ou projeto analisado.
- Problema de negócio e objetivo da análise.
- Alternativas avaliadas, incluindo o cenário Status Quo quando aplicável.
- Horizonte e periodicidade da análise.
- TMA e justificativa de sua utilização.
- Premissas técnicas, operacionais, comerciais e tributárias.
- Identificação dos dados informados, estimados e ainda não disponíveis.

### 2. Estrutura de Custos e Fluxo de Caixa

Apresente:
- Investimento inicial (FC0).
- Separação entre CapEx e OpEx.
- Classificação de custos diretos e indiretos.
- Receitas, despesas, impostos e investimentos adicionais.
- Valor residual e recuperação do capital de giro, quando aplicáveis.
- Tabela de fluxo de caixa por período.

Diferencie valores efetivamente informados de projeções e estimativas.

### 3. Indicadores de Viabilidade Econômica

Apresente os indicadores calculados pelo script scripts/calc_vpl_tir.py:

- Valor Presente Líquido (VPL).
- Taxa Interna de Retorno (TIR).
- Payback Simples.
- Payback Descontado.
- Índice de Lucratividade (IL).
- Indicadores de Unit Economics, quando aplicáveis.

Para cada indicador, apresente o resultado, sua unidade de medida e interpretação econômica.

Compare a TIR com a TMA quando a TIR for válida e disponível.

Utilize o VPL como principal critério de decisão econômica, considerando as limitações dos demais indicadores.

### 4. Eficiência Ágil e Priorização

Quando houver dados suficientes, apresente os resultados do script scripts/calc_gva.py:

**Gerenciamento de Valor Agregado:**
- Valor por Story Point (VSP).
- Valor Planejado (VPA).
- Valor Agregado (VAG).
- Custo Real (CR).
- Variação de Custo (VC).
- Variação de Prazo (VP).
- Índice de Desempenho de Custo (IDC).
- Índice de Desempenho de Prazo (IDP).
- Estimativa no Término (EAC).

**Priorização de Backlog:**
- Funcionalidades avaliadas.
- Critérios e pesos utilizados.
- Pontuações atribuídas.
- Ranking de prioridades.
- Justificativa das recomendações.

### 5. Modelo de Negócio e Proposta Econômica

Quando aplicável, apresente:
- Modelo de monetização recomendado.
- Estratégia de precificação.
- Margem de contribuição.
- Ponto de equilíbrio.
- CAC e LTV, quando houver dados suficientes.
- Custos de implantação e operação.
- Riscos comerciais e operacionais.

### 6. Análise de Riscos e Sensibilidade

Identifique as variáveis que mais influenciam os resultados econômicos.

Quando houver dados suficientes, apresente cenários otimista, base e pessimista, explicitando as alterações realizadas nas premissas.

Destaque riscos técnicos, financeiros, operacionais e de mercado, acompanhados de possíveis estratégias de mitigação.

### 7. Parecer Executivo

Finalize com uma recomendação objetiva:

- Aprovar: quando os indicadores e as premissas sustentarem a viabilidade.
- Rejeitar: quando a alternativa apresentar inviabilidade econômica fundamentada.
- Postergar: quando faltarem informações essenciais ou as condições atuais forem desfavoráveis.
- Priorizar: quando houver alternativas concorrentes e uma apresentar melhor atratividade econômica.

Toda recomendação deve ser justificada pelos resultados calculados, pelas premissas adotadas e pelos riscos identificados.

Nunca apresente resultados financeiros inventados ou indicadores não calculados pelos scripts disponíveis.

## Armadilhas Comuns (Gotchas)

Observe obrigatoriamente os seguintes cuidados durante as análises:

### 1. Custos Irreversíveis (Sunk Costs)

Valores já gastos e irrecuperáveis antes da decisão não devem influenciar a avaliação econômica incremental das alternativas futuras.

Considere apenas custos e benefícios futuros relevantes para a decisão.

### 2. Descasamento de Taxa e Período

Nunca desconte fluxos mensais utilizando uma TMA anual sem realizar a conversão para taxas equivalentes.

Fórmula de conversão:

i_mensal = (1 + i_anual)^(1/12) - 1

A taxa utilizada deve corresponder à periodicidade dos fluxos de caixa.

### 3. Inflação e Equação de Fisher

Não misture fluxos de caixa em moeda constante (reais) com taxas nominais (aparentes).

Utilize fluxos nominais com taxas nominais ou fluxos reais com taxas reais.

Quando necessário, aplique a equação de Fisher para converter as taxas.

### 4. Fluxos Não Convencionais e Limitações da TIR

Projetos de software podem apresentar múltiplas inversões de sinal devido a reinvestimentos, expansões ou custos extraordinários.

Essas situações podem produzir múltiplas TIRs ou ausência de uma solução válida.

Nesses casos, priorize o VPL como critério de decisão e explique as limitações da TIR.

### 5. Depreciação e Amortização

Depreciação e amortização são despesas contábeis, não saídas diretas de caixa.

Não desconte esses valores novamente no fluxo de caixa quando já estiverem contemplados na apuração do resultado operacional.

Considere seus efeitos tributários somente quando o regime fiscal e os dados disponíveis permitirem uma modelagem adequada.

### 6. Consistência Tributária

Não aplique alíquotas genéricas sem verificar o regime tributário, a atividade econômica e as condições específicas da empresa.

Consulte references/aliquotas.md e identifique as hipóteses utilizadas.

Diferencie alíquotas nominais de alíquotas efetivas.

### 7. Dados Insuficientes e Premissas

Não invente dados financeiros, comerciais ou operacionais.

Quando faltarem informações:
- Solicite os dados necessários.
- Identifique explicitamente as premissas adotadas.
- Utilize cenários estimados somente quando forem úteis e claramente identificados.
- Informe as limitações dos resultados.

### 8. Validação dos Cálculos

Utilize os scripts determinísticos disponíveis para os indicadores implementados.

Verifique se os parâmetros fornecidos são coerentes e se os resultados são matematicamente interpretáveis.

Não apresente um indicador como calculado quando o script não oferecer suporte à sua implementação.

### 9. Formatação Monetária e Matemática

Apresente valores monetários com identificação da moeda e separadores adequados.

Evite inserir o símbolo R$ dentro de blocos matemáticos delimitados por LaTeX quando isso comprometer a renderização.

### 10. Interpretação dos Indicadores

Não confunda:
- VPL positivo com garantia de sucesso comercial.
- TIR elevada com maior criação absoluta de riqueza.
- Payback curto com maior rentabilidade.
- Story Points entregues com valor de negócio efetivamente realizado.
- IDC e IDP favoráveis com garantia de cumprimento dos objetivos do produto.

Os indicadores devem ser interpretados em conjunto e dentro do contexto da decisão.
