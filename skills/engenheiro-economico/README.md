# Skill: Engenheiro Econômico (`engenheiro-economico`)

Skill padronizada no formato aberto **Agent Skills** (`engenheiro-economico`) projetada para capacitar líderes técnicos, Product Owners e engenheiros de software a modelar, calcular e defender a viabilidade financeira, a eficiência ágil e o *valuation* de sistemas de software.

## Propósito e Fundamentação Acadêmica

A skill operacionaliza os fundamentos das **12 aulas de Engenharia Econômica** em um fluxo determinístico auditável:
1. **Aulas 1 e 2:** Enquadramento decisório, restrições orçamentárias e trade-offs técnicos.
2. **Aulas 3 e 5:** Equivalência financeira (VP/VF), Taxa Mínima de Atratividade (TMA) e projeção de Fluxo de Caixa (CapEx, OpEx, capital de giro e valor residual).
3. **Aula 4:** Custos diretos e indiretos em TI, custos ocultos de qualidade/deploy ("iceberg") e precificação estratégica (Markup vs. Valor Percebido).
4. **Aulas 6 e 8:** Cálculo determinístico de VPL, TIR, Payback (simples e descontado), métricas SaaS (CAC, LTV, Ponto de Equilíbrio), depreciação de ativos de TI e impactos tributários.
5. **Aula 7:** Estruturação de propostas econômicas executivas e clareza de Propriedade Intelectual.
6. **Aula 9:** Gerenciamento de Valor Agregado (GVA / EVM) adaptado a Sprints e Story Points (VSP, VPA, VAG, CR, IDC, IDP e EAC).
7. **Aulas 10, 11 e 12:** Substituição de sistemas legados, princípio "Bom o Suficiente" e priorização econômica de backlog (Valor vs. Esforço).

## Arquitetura de Divulgação Progressiva

Para evitar desperdício de tokens e sobrecarga de contexto, a skill opera em três camadas:
- **Camada 1 (Catálogo):** O agente lê apenas `name` e `description` no YAML frontmatter (~85 tokens).
- **Camada 2 (Instruções):** O corpo de `SKILL.md` (< 5.000 tokens) é carregado somente quando a intenção do usuário exige modelagem econômica de software.
- **Camada 3 (Recursos e Scripts):** Os scripts Python (`scripts/calc_vpl_tir.py` e `scripts/calc_gva.py`), tabelas (`references/aliquotas.md`, `references/formulas.md`) e templates (`assets/proposta_executiva_template.md`) são acionados estritamente sob demanda.

## Plataforma Suportada e Instalação

Compatível com qualquer LLM ou *agent harness* aderente à especificação **Agent Skills** (Gemini CLI, Claude Code, OpenCode, Mistral AI Vibe, OpenHands, VS Code Copilot, Cursor, entre outros).

### Passo a Passo de Instalação e Carregamento
1. Crie o diretório da skill no repositório do projeto:
   ```bash
   mkdir -p .agents/skills/engenheiro-economico/{scripts,references,assets}