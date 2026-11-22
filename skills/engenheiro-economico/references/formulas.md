# Formulações Matemáticas de Engenharia Econômica em Software

Este documento reúne as principais fórmulas utilizadas pela skill
Engenheiro Econômico, com foco na análise de viabilidade financeira,
precificação, produtos digitais, gerenciamento de valor agregado e
substituição de sistemas legados.

## 1. Valor do Dinheiro no Tempo (TVM)

O Valor do Dinheiro no Tempo considera que um recurso financeiro possui
valor diferente conforme o momento em que está disponível.

- **Valor Futuro (VF):**
  `VF = VP * (1 + i)^n`

- **Valor Presente (VP):**
  `VP = VF / (1 + i)^n`

Onde:
- `VP`: valor presente.
- `VF`: valor futuro.
- `i`: taxa de juros efetiva por período.
- `n`: número de períodos.

**Taxa Mínima de Atratividade (TMA):**

Taxa mínima de retorno exigida para aceitar um investimento, refletindo
o custo de oportunidade do capital e os riscos associados ao projeto.

A TMA deve ser compatível com:
- O período dos fluxos de caixa (mensal, anual etc.).
- A natureza nominal ou real dos valores projetados.
- O risco do investimento e o custo de oportunidade do capital.

Não se deve misturar taxas anuais com fluxos mensais sem realizar a
conversão adequada.

## 2. Indicadores de Viabilidade e Valuation

### Valor Presente Líquido (VPL)

`VPL = Soma de [ FC_t / (1 + TMA)^t ] para t = 0 até n`

Onde:
- `FC_t`: fluxo de caixa líquido no período t.
- `TMA`: taxa mínima de atratividade.
- `n`: número total de períodos.

**Critério de decisão:**
- `VPL > 0`: o projeto gera valor acima do retorno mínimo exigido.
- `VPL = 0`: o projeto remunera exatamente a TMA.
- `VPL < 0`: o projeto não atinge o retorno mínimo exigido.

O VPL é o principal critério de avaliação econômica utilizado pela skill.

### Taxa Interna de Retorno (TIR)

Taxa `r` que torna o VPL igual a zero:

`Soma de [ FC_t / (1 + r)^t ] = 0`

**Critério complementar de decisão:**
- `TIR > TMA`: retorno superior à taxa mínima exigida.
- `TIR = TMA`: retorno igual à taxa mínima exigida.
- `TIR < TMA`: retorno inferior à taxa mínima exigida.

A TIR deve ser interpretada em conjunto com o VPL. Fluxos de caixa
não convencionais podem apresentar múltiplas TIRs ou nenhuma solução
real, tornando sua interpretação limitada.

### Payback Simples

Representa o período necessário para recuperar o investimento inicial,
sem considerar o valor do dinheiro no tempo.

É identificado pelo primeiro período em que:

`Soma de FC_t >= 0`

Considerando a soma acumulada desde `t = 0`.

### Payback Descontado

Representa o período necessário para recuperar o investimento inicial,
considerando o valor do dinheiro no tempo.

É identificado pelo primeiro período `k` em que:

`Soma de [ FC_t / (1 + TMA)^t ] >= 0`

Considerando a soma acumulada desde `t = 0`.

Quando o retorno ocorre entre dois períodos, pode-se estimar uma fração
do período por interpolação.

O Payback, simples ou descontado, não substitui o VPL, pois não considera
integralmente os fluxos posteriores à recuperação do investimento.

### Índice de Lucratividade (IL): benefício/custo abrangente

A implementação da skill utiliza a razão entre o valor presente de todos
os benefícios de caixa considerados e o valor presente de todos os custos
e desembolsos considerados:

`IL = VP(benefícios) / VP(custos e desembolsos)`

Cada valor é descontado no período em que ocorre:

`VP(X) = soma_t [ X_t / (1 + TMA)^t ]`

**Benefícios:** receita bruta líquida dos tributos simplificados, valor
residual, recuperação do capital de giro e outras entradas de caixa que
existam no modelo.

**Custos e desembolsos:** CapEx inicial, capital de giro inicial, OpEx e
CapEx adicional de cada período. Benefícios e custos são classificados
separadamente antes do desconto. Cada componente entra uma única vez:
por exemplo, OpEx é um custo e não deve também ser deduzido dos benefícios.

**Casos especiais:** se o VP dos custos for zero, o IL é indefinido e o
script retorna `null`; se o VP dos benefícios for zero e o VP dos custos
for positivo, o IL é zero.

**Distinção da formulação tradicional:** em projetos com investimento
concentrado no período inicial, uma formulação tradicional é
`IL_tradicional = (VPL + |I_0|) / |I_0|`, em que `I_0` é o investimento
inicial. Essa razão pode equivaler a benefícios presentes divididos pelo
investimento inicial sob as hipóteses dessa formulação. Ela não é a mesma
medida abrangente implementada aqui quando há OpEx, capital de giro,
investimentos adicionais ou outros desembolsos. O IL benefício/custo
abrangente inclui esses custos no denominador e deve ser interpretado
junto ao VPL.

**Critério de leitura:** IL > 1 indica VP dos benefícios superior ao VP
dos custos considerados; IL = 1 indica igualdade; IL < 1 indica VP dos
benefícios inferior ao VP dos custos. O VPL permanece o critério
principal de decisão econômica.

## 3. Métricas de Produtos Digitais (SaaS) e Precificação

### Margem de Contribuição Unitária (MC)

`MC = Preço_Unitário - Custo_Variável_Unitário`

Representa o valor que cada unidade comercializada contribui para
cobrir os custos fixos e gerar resultado operacional.

A margem percentual é:

`MC_percentual = MC / Preço_Unitário`

### Ponto de Equilíbrio (Break-Even)

Quantidade mínima de unidades que precisam ser comercializadas para
cobrir os custos fixos.

`PE_unidades = Custos_Fixos / MC`

Quando os gastos de marketing e vendas forem tratados como custos fixos
do período:

`PE_unidades = (Custos_Fixos + Marketing_Vendas) / MC`

O resultado deve ser arredondado para cima quando representar uma
quantidade mínima de clientes ou unidades.

A receita, os custos fixos e os custos variáveis devem utilizar a mesma
unidade de tempo, por exemplo, valores mensais.

### Custo de Aquisição de Cliente (CAC)

`CAC = Despesas_Marketing_e_Vendas / Novos_Clientes_Adquiridos`

Representa o investimento médio necessário para conquistar um novo
cliente.

Os gastos e a quantidade de novos clientes devem corresponder ao mesmo
período ou critério de apuração.

### Lifetime Value (LTV)

Estimativa do valor de contribuição econômica gerado por um cliente
durante seu relacionamento com a empresa.

`LTV = (Ticket_Médio_Mensal * Margem_Contribuição_Percentual) / Churn_Mensal`

Premissas:
- O ticket médio representa a receita mensal média por cliente.
- A margem de contribuição percentual representa a parcela da receita
  que permanece após os custos variáveis considerados.
- O churn deve ser uma taxa mensal, expressa em formato decimal.
- A margem e o churn são considerados constantes ao longo do tempo.

Essa é uma estimativa simplificada. Ela não considera, por exemplo,
descontos financeiros, variações de consumo ou alterações futuras
no comportamento dos clientes.

### Relação LTV/CAC

`LTV_CAC = LTV / CAC`

Compara o valor econômico estimado de um cliente com o custo necessário
para adquiri-lo.

Deve ser interpretado junto às premissas utilizadas no cálculo de LTV
e CAC, não como garantia de rentabilidade.

### Precificação por Markup

`Preço_Unitário = Custo_Unitário * (1 + Markup)`

O markup representa um percentual aplicado sobre o custo unitário.

Exemplo:
- Custo unitário: R$ 100,00.
- Markup: 30%.
- Preço calculado: R$ 130,00.

Essa é uma fórmula simplificada. Uma formação de preço completa pode
exigir a inclusão de tributos, comissões, despesas operacionais e
margem desejada sobre o preço de venda.

## 4. Gerenciamento de Valor Agregado (GVA / EVM) no Ágil

O Gerenciamento de Valor Agregado integra escopo, prazo e custos para
acompanhar o desempenho de um projeto.

Na adaptação utilizada pela skill, os Story Points são empregados como
referência proporcional para distribuir o orçamento do projeto.

**Atenção:** Story Points são medidas relativas de estimativa de
complexidade e esforço, não unidades monetárias. A conversão abaixo
constitui uma aproximação gerencial e depende de uma baseline de escopo
e orçamento consistente. Não deve ser interpretada como equivalência
financeira universal entre Story Points.

### Valor por Story Point (VSP)

`VSP = BAC / Total_SP_Planejados`

Onde:
- `BAC`: orçamento total aprovado do projeto.
- `Total_SP_Planejados`: quantidade total de Story Points da baseline.

### Valor Planejado (VPA / PV)

`VPA = SP_planejados * VSP`

Representa o valor orçamentário associado ao trabalho que deveria estar
concluído até a data de análise.

### Valor Agregado (VAG / EV)

`VAG = SP_entregues * VSP`

Representa o valor orçamentário associado ao trabalho efetivamente
concluído até a data de análise.

### Custo Real (CR / AC)

`CR = Horas_Trabalhadas * Custo_Hora`

Representa o custo efetivamente incorrido para executar o trabalho.

Outros custos diretos e indiretos devem ser incluídos quando fizerem
parte da estrutura de custos utilizada na análise.

### Variação de Custo (VC / CV)

`VC = VAG - CR`

Interpretação:
- `VC > 0`: trabalho executado abaixo do custo orçado correspondente.
- `VC = 0`: desempenho exatamente dentro do custo previsto.
- `VC < 0`: custo superior ao valor agregado.

### Variação de Prazo (VPZ / SV)

`VPZ = VAG - VPA`

Interpretação:
- `VPZ > 0`: mais valor foi agregado do que o planejado até a data.
- `VPZ = 0`: execução alinhada ao planejamento.
- `VPZ < 0`: menos valor foi agregado do que o planejado.

### Índice de Desempenho de Custo (IDC / CPI)

`IDC = VAG / CR`

Interpretação:
- `IDC > 1`: desempenho favorável de custo.
- `IDC = 1`: desempenho conforme o orçamento.
- `IDC < 1`: desempenho desfavorável de custo.

### Índice de Desempenho de Prazo (IDP / SPI)

`IDP = VAG / VPA`

Interpretação:
- `IDP > 1`: execução adiantada em relação ao planejamento.
- `IDP = 1`: execução alinhada ao planejamento.
- `IDP < 1`: execução atrasada em relação ao planejamento.

O IDP representa a relação entre valor agregado e valor planejado.
Não representa diretamente a quantidade de dias de atraso ou
adiantamento.

### Estimativa no Término (EAC)

Projeção do custo total do projeto ao término, considerando diferentes
hipóteses de desempenho futuro.

**Método 1 — Desempenho de custo:**

`EAC = BAC / IDC`

Utilizado quando se considera que o desempenho de custo observado
continuará durante o restante do projeto.

**Método 2 — Orçamento restante:**

`EAC = CR + (BAC - VAG)`

Utilizado quando se considera que o trabalho restante será executado
conforme o orçamento originalmente planejado.

**Método 3 — Desempenho combinado:**

`EAC = CR + (BAC - VAG) / (IDC * IDP)`

Utilizado quando se considera que tanto o desempenho de custo quanto
o desempenho de prazo influenciarão o custo do trabalho restante.

Os métodos são estimativas alternativas. A escolha deve refletir
a hipótese de desempenho futuro mais adequada ao projeto.

### Estimativa para Conclusão (ETC)

`ETC = EAC - CR`

Representa o custo estimado necessário para concluir o trabalho restante.

### Variação no Término (VAC)

`VAC = BAC - EAC`

Interpretação:
- `VAC > 0`: previsão de conclusão abaixo do orçamento.
- `VAC = 0`: previsão de conclusão dentro do orçamento.
- `VAC < 0`: previsão de conclusão acima do orçamento.

**Limitações:** IDC e IDP não podem ser calculados quando seus
denominadores forem iguais a zero. Nesses casos, os indicadores devem
ser tratados como indefinidos, e não como zero.

## 5. Substituição e Aposentadoria de Sistemas Legados

### Custo Anual Equivalente (CAE)

O CAE converte o valor presente de custos de uma alternativa em uma
série uniforme de custos anuais equivalentes.

`CAE = VP_Custos * [ i * (1 + i)^n ] / [ (1 + i)^n - 1 ]`

Onde:
- `VP_Custos`: valor presente dos custos da alternativa.
- `i`: taxa efetiva por período.
- `n`: número de períodos da análise.

Na composição do valor presente dos custos, devem ser considerados,
quando aplicáveis:
- Investimento inicial de implantação e migração.
- Custos de operação e manutenção.
- Custos de infraestrutura e licenciamento.
- Custos de suporte e evolução.
- Custos de substituição de componentes.
- Valor residual, descontado dos custos.

**Critério de decisão:**

Quando as alternativas oferecem capacidade e nível de serviço
comparáveis, e são avaliadas sob premissas equivalentes:

`CAE_novo < CAE_legado`

Indica que a alternativa nova possui menor custo anual equivalente.

A análise também deve considerar riscos de indisponibilidade,
obsolescência tecnológica, segurança, manutenção corretiva, dependência
de fornecedores e custos de oportunidade.

Quando as alternativas possuem vidas úteis diferentes, deve-se adotar
um horizonte de análise comum ou uma hipótese explícita de repetição
dos ciclos de substituição.
