# Engenheiro Econômico

**Skill de IA especializada em Engenharia Econômica aplicada a Projetos de Software.**

## 1. Sobre o projeto

O Engenheiro Econômico é uma Skill de IA desenvolvida para apoiar decisões econômicas e financeiras relacionadas a projetos de software.

Seu objetivo é auxiliar profissionais de tecnologia, líderes técnicos, Product Owners e gestores na avaliação de investimentos, análise de viabilidade, planejamento financeiro, acompanhamento de desempenho e priorização de funcionalidades.

A solução combina instruções especializadas, referências conceituais e scripts Python para apoiar análises fundamentadas e transparentes.

## 2. Objetivos

- Avaliar a viabilidade econômica de projetos de software.
- Estruturar projeções de fluxo de caixa e investimentos.
- Calcular indicadores financeiros, como VPL, TIR, Payback e Índice de Lucratividade.
- Analisar custos, receitas, precificação e modelos de negócio SaaS.
- Calcular indicadores de Unit Economics, como CAC, LTV e LTV/CAC.
- Aplicar Gerenciamento de Valor Agregado (GVA/EVM) ao desenvolvimento ágil.
- Apoiar a priorização econômica de funcionalidades.
- Elaborar propostas e relatórios executivos para apoiar decisões.

## 3. Tecnologias e compatibilidade

- **Agent Skills:** formato aberto de organização de instruções para agentes de IA.
- **Python 3.8+:** execução dos scripts de cálculo.
- **Biblioteca padrão Python:** não são necessárias dependências externas.
- **Codex CLI:** ambiente utilizado para desenvolvimento e validação da skill.

A estrutura foi projetada para ser compatível com ambientes que suportam Agent Skills, respeitando as convenções de descoberta e carregamento de instruções do agente utilizado.

## 4. Estrutura do projeto

```text
engenheiro-economico/
├── README.md
└── skills/
    └── engenheiro-economico/
        ├── SKILL.md
        ├── assets/
        │   └── proposta_executiva_template.md
        ├── references/
        │   ├── aliquotas.md
        │   └── formulas.md
        └── scripts/
            ├── calc_gva.py
            └── calc_vpl_tir.py
```

### Descrição dos componentes

| Componente | Responsabilidade |
|---|---|
| SKILL.md | Instruções, fluxo de trabalho e critérios de análise da IA |
| references/formulas.md | Fórmulas e conceitos de Engenharia Econômica |
| references/aliquotas.md | Referências de alíquotas utilizadas no modelo simplificado |
| assets/proposta_executiva_template.md | Modelo de proposta econômica |
| scripts/calc_vpl_tir.py | Cálculos de fluxo de caixa e viabilidade financeira |
| scripts/calc_gva.py | Cálculos de GVA/EVM e priorização do backlog |

## 5. Funcionalidades

### 5.1. Análise de viabilidade financeira

O módulo financeiro permite calcular:

- Fluxo de caixa líquido.
- Valor Presente Líquido (VPL).
- Taxa Interna de Retorno (TIR).
- Payback simples e descontado.
- Índice de Lucratividade.
- Ponto de equilíbrio.
- CAC, LTV e relação LTV/CAC.

### 5.2. Gerenciamento de Valor Agregado

O módulo de GVA/EVM permite acompanhar:

- Valor Planejado (VPA).
- Valor Agregado (VAG).
- Custo Real (CR).
- Variação de Custo (VC).
- Variação de Prazo (VPZ).
- Índices de desempenho de custo e prazo (IDC e IDP).
- Estimativa no Término (EAC).
- Estimativa para Terminar (ETC).
- Variação no Término (VAC).

A conversão de Story Points em valores monetários é uma aproximação gerencial baseada na distribuição proporcional do orçamento. Não representa uma equivalência financeira intrínseca dos Story Points.

### 5.3. Priorização do backlog

O módulo permite classificar funcionalidades conforme critérios ponderados de benefício e sacrifício:

- Valor de negócio.
- Alinhamento estratégico.
- Redução de risco.
- Esforço.
- Custo.

O resultado é um índice multicritério de prioridade, não um ROI financeiro.

## 6. Instalação e utilização

### 6.1. Requisitos

- Python 3.8 ou superior.
- Ambiente de agente de IA compatível com Agent Skills.
- Suporte à descoberta de skills no diretório `.agents/skills/`.

### 6.2. Instalação

No repositório, a Skill está localizada em skills/engenheiro-economico/.

Para instalá-la em um projeto que utiliza o padrão Agent Skills, copie essa pasta para o diretório de descoberta do ambiente:

```text
.agents/skills/engenheiro-economico/
```

Após a cópia, a estrutura no projeto de destino deverá conter o arquivo SKILL.md diretamente dentro da pasta engenheiro-economico, acompanhado dos diretórios assets, references e scripts.

No Codex CLI, abra o ambiente do projeto e verifique a disponibilidade da Skill por meio do comando:

```text
/skills
```

Selecione ou acione a skill conforme os recursos do ambiente.

### 6.3. Execução dos scripts

Os scripts podem ser executados independentemente da interação com a IA.

Análise financeira:

```powershell
py .\.agents\skills\engenheiro-economico\scripts\calc_vpl_tir.py --file .\caminho\para\entrada_financeira.json
```

GVA e priorização do backlog:

```powershell
py .\.agents\skills\engenheiro-economico\scripts\calc_gva.py --file .\caminho\para\entrada_gva_backlog.json
```

Os caminhos apresentados são ilustrativos. Os arquivos JSON devem ser preparados pelo usuário conforme os parâmetros esperados por cada script.

Ambos aceitam entradas JSON por arquivo, argumento de linha de comando ou entrada padrão.

### 6.4. Exemplos de acionamento

**Viabilidade financeira**

> Analise a viabilidade econômica deste projeto de software. Considere investimento inicial, custos operacionais, receitas projetadas e TMA. Calcule VPL, TIR e Payback, interprete os resultados e apresente um parecer.

**Modelo SaaS**

> Avalie a sustentabilidade comercial deste produto SaaS. Analise margem de contribuição, ponto de equilíbrio, CAC, LTV e relação LTV/CAC.

**Acompanhamento ágil**

> Analise o desempenho econômico deste projeto utilizando GVA/EVM. Avalie custo, prazo e projeção de orçamento no término.

**Priorização de funcionalidades**

> Analise este backlog considerando valor de negócio, alinhamento estratégico, redução de risco, esforço e custo. Apresente um ranking justificado.

**Proposta executiva**

> Elabore uma proposta econômica executiva para este projeto de software, apresentando premissas, investimentos, indicadores financeiros, riscos e recomendação.

## 7. Limitações e premissas

Os resultados dependem da qualidade e consistência dos dados fornecidos.

As principais simplificações da versão inicial são:

- O modelo tributário aplica uma alíquota diretamente sobre a receita bruta, não substituindo uma apuração tributária completa.
- Depreciação e amortização não são modeladas nos cálculos financeiros atuais.
- A conversão de Story Points em valor monetário é uma aproximação gerencial.
- A priorização do backlog utiliza um modelo multicritério, não uma avaliação de retorno financeiro.
- Os indicadores de Unit Economics utilizam hipóteses simplificadas de churn, margem e aquisição de clientes.
- A estimativa de TIR é numérica e pode não identificar todas as raízes possíveis de fluxos não convencionais.
- As análises produzidas pela IA não substituem avaliação contábil, tributária, jurídica ou financeira especializada.

## 8. Considerações finais

O Engenheiro Econômico busca aproximar Engenharia de Software e Engenharia Econômica, oferecendo uma ferramenta de apoio à tomada de decisão.

A proposta é transformar dados técnicos, operacionais e financeiros em informações estruturadas que auxiliem a avaliar investimentos, compreender riscos e justificar decisões relacionadas ao ciclo de vida de produtos de software.

A versão inicial prioriza transparência das premissas, rastreabilidade dos cálculos e interpretação gerencial dos resultados.