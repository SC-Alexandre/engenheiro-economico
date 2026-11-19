# Formulações Matemáticas de Engenharia Econômica em Software

## 1. Valor do Dinheiro no Tempo (TVM)
- **Valor Futuro (VF):** `VF = VP * (1 + i)^n`
- **Valor Presente (VP):** `VP = VF / (1 + i)^n`
- **Taxa Mínima de Atratividade (TMA):** Taxa mínima exigida para aceitar o projeto, refletindo o custo de oportunidade do capital mais o prêmio de risco tecnológico/mercado.

## 2. Indicadores de Viabilidade e Valuation
- **Valor Presente Líquido (VPL):**
  `VPL = Soma de [ FC_t / (1 + TMA)^t ] para t = 0 até n`
  Critério: `VPL > 0` indica que o projeto cria riqueza líquida acima do custo de oportunidade.
- **Taxa Interna de Retorno (TIR):**
  Taxa `r` que iguala o VPL a zero: `Soma de [ FC_t / (1 + r)^t ] = 0`
  Critério: `TIR > TMA` indica que o projeto é economicamente atrativo.
- **Payback Descontado:**
  Menor período `k` no qual a soma dos fluxos descontados `Soma de [ FC_t / (1 + TMA)^t ] >= 0`.
- **Índice de Lucratividade (IL):**
  `IL = (VPL + |I_0|) / |I_0|`

## 3. Métricas de Produtos Digitais (SaaS) e Precificação
- **Margem de Contribuição Unitária (MC):** `MC = Preço_Unitário - Custo_Variável_Unitário`
- **Ponto de Equilíbrio (Break-Even):** `PE_unidades = Custos_Fixos / (Preço_Unitário - Custo_Variável_Unitário)`
- **Custo de Aquisição de Cliente (CAC):** `CAC = Despesas_Marketing_e_Vendas / Novos_Clientes_Adquiridos`
- **Lifetime Value (LTV):** `LTV = (Ticket_Médio * Margem_Bruta_Percentual) / Churn_Mensal`
- **Precificação por Markup:** `Preço = Custo_Unitário * (1 + Markup)`

## 4. Gerenciamento de Valor Agregado (GVA / EVM) no Ágil
- **Valor por Story Point (VSP):** `VSP = BAC / Total_SP_Planejados`
- **Valor Planejado (VPA):** `VPA = SP_planejados * VSP`
- **Valor Agregado (VAG):** `VAG = SP_entregues * VSP`
- **Custo Real (CR):** `CR = Horas_Trabalhadas * Custo_Hora`
- **Índice de Desempenho de Custo (IDC / CPI):** `IDC = VAG / CR`
- **Índice de Desempenho de Prazo (IDP / SPI):** `IDP = VAG / VPA`
- **Estimativa no Término (EAC):** `EAC = BAC / IDC`

## 5. Substituição e Aposentadoria de Sistemas Legados
- **Custo Anual Equivalente (CAE):**
  `CAE = VPL_custos * [ i * (1 + i)^n ] / [ (1 + i)^n - 1 ]`
  Critério: Substitui-se o sistema legado quando `CAE_novo < CAE_legado` (considerando manutenção corretiva crescente, risco de indisponibilidade e custo de oportunidade).