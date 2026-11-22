# Tabelas de Tributação, Encargos e Depreciação em TI (Brasil)

Este documento apresenta parâmetros tributários e trabalhistas de
referência para modelagens econômicas de projetos de software,
desenvolvimento de sistemas e produtos SaaS no Brasil.

As alíquotas e percentuais apresentados são referências educacionais,
não substituindo a análise contábil e tributária específica de cada
empresa.

**Data de referência: novembro de 2026.**

Os valores devem ser revalidados sempre que houver alteração legislativa,
mudança de regime tributário ou mudança no município de incidência.

## 1. Regimes Tributários para Empresas de Software / SaaS

### A. Simples Nacional (LC 123/2006)

Atividades como elaboração de programas de computador, licenciamento
ou cessão de direito de uso de programas de computação e determinados
serviços relacionados à tecnologia podem estar sujeitas ao Fator R.

O Fator R corresponde à relação entre a folha de salários dos últimos
12 meses e a receita bruta dos últimos 12 meses.

`Fator R = Folha_de_Salarios_12m / Receita_Bruta_12m`

Para essa finalidade, a folha considera os valores previstos na
legislação, incluindo remunerações, pró-labore, contribuição patronal
previdenciária e FGTS.

**Enquadramento:**

- Fator R >= 28%: tributação pelo Anexo III.
- Fator R < 28%: tributação pelo Anexo V.

**Anexo III — alíquotas nominais de referência:**

| Receita bruta em 12 meses | Alíquota nominal | Parcela a deduzir |
|---|---:|---:|
| Até R$ 180.000,00 | 6,00% | R$ 0,00 |
| R$ 180.000,01 a R$ 360.000,00 | 11,20% | R$ 9.360,00 |
| R$ 360.000,01 a R$ 720.000,00 | 13,50% | R$ 17.640,00 |

**Anexo V — alíquotas nominais de referência:**

| Receita bruta em 12 meses | Alíquota nominal | Parcela a deduzir |
|---|---:|---:|
| Até R$ 180.000,00 | 15,50% | R$ 0,00 |
| R$ 180.000,01 a R$ 360.000,00 | 18,00% | R$ 4.500,00 |
| R$ 360.000,01 a R$ 720.000,00 | 19,50% | R$ 9.900,00 |

**Cálculo da alíquota efetiva:**

`Aliquota_Efetiva = (RBT12 * Aliquota_Nominal - Parcela_Deduzir) / RBT12`

Onde `RBT12` representa a receita bruta acumulada nos últimos
12 meses.

A alíquota efetiva é utilizada para calcular o valor devido no
período de apuração, observadas as regras do Simples Nacional.

**Atenção:** as tabelas acima apresentam apenas as três primeiras
faixas para fins de referência. O cálculo completo deve considerar
todas as faixas, limites, repartições e regras vigentes no período.

### B. Lucro Presumido — Serviços de TI

Para uma modelagem simplificada de prestação de serviços de TI,
pode-se considerar uma presunção de 32% sobre a receita bruta,
desde que essa classificação seja aplicável à atividade exercida.

**Tributos de referência:**

- ISS (Municipal): alíquota geralmente entre 2% e 5%, conforme a
  legislação do município e o serviço enquadrado.
- PIS (Regime Cumulativo): 0,65% sobre a receita.
- COFINS (Regime Cumulativo): 3,00% sobre a receita.
- IRPJ: alíquota de 15% sobre a base presumida.
- CSLL: alíquota geral de 9% sobre a base presumida.

**Cálculo simplificado do IRPJ e CSLL:**

IRPJ:
`32% * 15% = 4,80% sobre a receita bruta`

CSLL:
`32% * 9% = 2,88% sobre a receita bruta`

Total de IRPJ e CSLL:
`4,80% + 2,88% = 7,68%`

**Carga tributária estimada:**

`Carga = ISS + PIS + COFINS + IRPJ + CSLL`

Considerando ISS entre 2% e 5%:

- Carga estimada mínima: 13,33%.
- Carga estimada máxima: 16,33%.

**Limitações dessa estimativa:**

- O adicional de IRPJ de 10% deve ser considerado sobre a parcela
  da base de cálculo que exceder R$ 20.000,00 por mês do período
  de apuração.
- O ISS depende da legislação municipal e da classificação do serviço.
- A presunção de 32% deve ser confirmada conforme a atividade.
- A estimativa não contempla todas as particularidades fiscais,
  retenções, incentivos ou regimes especiais.

Os valores apresentados representam uma aproximação para modelagem,
não uma apuração tributária completa.

### C. Transição da Reforma Tributária

A partir de 2026, inicia-se a transição para o novo modelo de tributação
sobre o consumo, com implantação gradual da CBS e do IBS.

**Referência para 2026:**

- CBS: 0,9% em fase de teste.
- IBS: 0,1% em fase de teste.

Os valores recolhidos na fase de teste podem ser compensados com
PIS e COFINS, conforme as condições previstas na legislação.

A partir de 2027, ocorre a extinção de PIS e COFINS e o avanço da
implantação da CBS e do IBS.

**Orientação para modelagem econômica:**

Não se deve somar automaticamente as alíquotas de teste da CBS e
do IBS à carga tributária anterior.

Projetos com horizonte financeiro que ultrapasse 2026 devem considerar
a transição tributária e revisar as premissas de tributação de cada
período projetado.

## 2. Encargos sobre Mão de Obra Técnica (Custo/Hora)

O custo de um profissional de TI deve considerar não apenas o salário
ou valor contratado, mas também os encargos, benefícios, provisões
e custos operacionais relacionados à contratação.

### A. Contratação CLT

**Provisões trabalhistas de referência:**

- 13º salário: aproximadamente 8,33% ao mês, correspondente à
  provisão de 1/12 da remuneração.
- Férias e adicional constitucional de 1/3: provisão que deve
  considerar a metodologia de cálculo adotada. Uma estimativa
  simplificada de 1/12 da remuneração acrescida de 1/3 corresponde
  a aproximadamente 11,11%.
- FGTS: depósito de 8% sobre a remuneração, observadas as bases
  legais, incluindo a gratificação natalina.

A multa rescisória de 40% do FGTS está relacionada à demissão
sem justa causa e não deve ser tratada como encargo mensal
universal e obrigatório.

**Outros encargos e custos:**

- Contribuição previdenciária patronal, quando aplicável.
- RAT e contribuições destinadas a terceiros, conforme o regime
  tributário e o enquadramento da empresa.
- Benefícios, equipamentos, licenças, treinamento e infraestrutura.
- Custos de recrutamento, integração e administração de pessoal.

**Particularidade do Simples Nacional:**

A Contribuição Patronal Previdenciária (CPP) normalmente integra
o recolhimento do DAS, exceto nas atividades legalmente enquadradas
no Anexo IV.

Por isso, a composição do custo de um profissional CLT deve considerar
o regime tributário da empresa, evitando duplicar encargos já incluídos
no Simples Nacional.

Não existe um percentual único de encargos trabalhistas aplicável
a todas as empresas de TI.

### B. Contratação PJ / Prestação de Serviços

Para profissionais contratados como pessoa jurídica, considerar:

- Valor contratado por hora, mês ou entrega.
- Tributos e encargos incidentes sobre a prestação de serviços.
- Custos de gestão contratual e administração.
- Ferramentas, licenças e infraestrutura fornecidas pela contratante.
- Eventuais custos de integração, substituição e continuidade
  do serviço.

O valor contratado deve ser tratado como custo de prestação
de serviços, sem aplicação automática dos encargos típicos
de uma contratação CLT.

## 3. Depreciação e Amortização de Ativos de TI

A depreciação e a amortização representam a apropriação sistemática
do valor de determinados ativos ao longo de sua vida útil.

### A. Hardware e Equipamentos de Processamento de Dados

Para computadores e periféricos, a referência fiscal tradicional é:

- Vida útil: 5 anos.
- Taxa anual: 20%.
- Método de referência: linear.

`Depreciacao_Anual = Valor_Contabil_Ativo / Vida_Util_Anos`

O valor acumulado da depreciação não pode ultrapassar o custo
de aquisição do bem, observadas as regras fiscais aplicáveis.

### B. Software Adquirido e Desenvolvimento Capitalizado

Para custos e despesas de aquisição e desenvolvimento de software
utilizados em processamento de dados, a referência fiscal tradicional
estabelece prazo mínimo de amortização de cinco anos.

- Prazo de referência: 5 anos.
- Taxa anual de referência: 20%.
- Método de referência: linear.

`Amortizacao_Anual = Valor_Ativado / Prazo_Amortizacao_Anos`

A capitalização depende do atendimento aos critérios contábeis
e fiscais aplicáveis. Nem todo gasto com desenvolvimento de software
deve ser automaticamente reconhecido como ativo intangível.

A vida útil contábil pode exigir avaliação própria e não deve ser
confundida automaticamente com o prazo fiscal de amortização.

### C. Efeito no Fluxo de Caixa e na Tributação

A depreciação e a amortização não representam, por si mesmas,
uma saída de caixa no período em que são reconhecidas.

Seus efeitos econômicos e tributários incluem:

- Redução do resultado contábil.
- Possível redução do lucro tributável.
- Benefício fiscal potencial em empresas no Lucro Real,
  observados os requisitos legais.
- Necessidade de controle de diferenças entre critérios contábeis
  e fiscais, quando existentes.

No Simples Nacional e no Lucro Presumido, não se deve presumir
que a depreciação ou amortização produzirá automaticamente uma
redução do tributo calculado sobre a receita ou sobre a base presumida.

## 4. Orientações de Uso pela Skill

As informações deste documento devem ser utilizadas como parâmetros
de referência, e não como substitutas de uma apuração contábil.

Ao realizar uma análise econômica, a skill deve:

1. Identificar o regime tributário considerado.
2. Identificar o município quando houver incidência de ISS.
3. Solicitar ou explicitar as premissas tributárias utilizadas.
4. Verificar a compatibilidade entre o período dos fluxos de caixa
   e os períodos de apuração dos tributos.
5. Distinguir alíquotas nominais de alíquotas efetivas.
6. Considerar a transição da reforma tributária em projeções
   que ultrapassem 2026.
7. Evitar aplicar percentuais genéricos de encargos CLT sem
   justificar sua composição.
8. Informar quando uma taxa for apenas uma estimativa simplificada.

**Limitação do script calc_vpl_tir.py:**

O parâmetro `aliquota_imposto` representa uma alíquota simplificada
aplicada diretamente sobre a receita bruta dos períodos.

O script não realiza a apuração completa de tributos de um regime
específico, não calcula separadamente todos os tributos e não
considera automaticamente as particularidades do Simples Nacional,
Lucro Presumido, Lucro Real ou da transição da reforma tributária.

Por isso, a alíquota fornecida deve ser tratada como uma premissa
estimada de tributação sobre receita, explicitamente informada
pelo usuário.

A skill deve deixar essa simplificação clara sempre que apresentar
resultados financeiros baseados nesse parâmetro.

## 5. Fontes Oficiais para Consulta

- Lei Complementar nº 123/2006 — Simples Nacional:
  https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm

- Resolução CGSN nº 140/2018 — regulamentação do Simples Nacional:
  https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=92278

- Lei nº 9.249/1995 — IRPJ e CSLL:
  https://www.planalto.gov.br/ccivil_03/leis/l9249.htm

- Lei Complementar nº 116/2003 — ISS:
  https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp116.htm

- Lei nº 8.036/1990 — FGTS:
  https://www.planalto.gov.br/ccivil_03/leis/l8036compilada.htm

- Instrução Normativa RFB nº 1.700/2017 — depreciação e amortização:
  https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=81268

- Receita Federal — Reforma Tributária do Consumo:
  https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/reforma-tributaria-do-consumo/entenda

- Receita Federal — Perguntas e Respostas Pessoa Jurídica:
  https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/declaracoes-e-demonstrativos/ecf