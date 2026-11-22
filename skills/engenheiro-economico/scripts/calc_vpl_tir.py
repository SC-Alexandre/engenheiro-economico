#!/usr/bin/env python3
"""
Calculadora de Engenharia Econômica aplicada a Projetos de Software.

Calcula:
- Fluxo de Caixa Líquido;
- Valor Presente Líquido (VPL);
- Taxa Interna de Retorno (TIR);
- Payback Simples;
- Payback Descontado;
- Índice de Lucratividade (IL);
- Ponto de Equilíbrio;
- CAC, LTV e relação LTV/CAC.

Compatibilidade: Python 3.8+
Dependências: somente biblioteca padrão.

Modelo tributário:
A alíquota informada em "aliquota_imposto" é aplicada diretamente
sobre a receita bruta. Trata-se de uma simplificação para modelagem
econômica, não de uma apuração tributária completa.

Execução:
    py calc_vpl_tir.py --file dados.json
    py calc_vpl_tir.py --json '{"tma": 0.12, ...}'
    py calc_vpl_tir.py < dados.json
"""

import argparse
import json
import math
import sys
from typing import Any, Dict, List, Optional


class CalculadoraEngenhariaEconomica:
    """
    Centraliza os cálculos de Engenharia Econômica para projetos
    de software.

    A classe valida os dados recebidos, constrói o fluxo de caixa
    e calcula os indicadores financeiros e de Unit Economics.

    Convenções:
    - FC0 representa o investimento inicial.
    - A TMA deve estar na mesma periodicidade dos fluxos.
    - As receitas e despesas são consideradas no fim de cada período.
    - O capital de giro é investido no período zero e recuperado
      integralmente no último período.
    - O valor residual é recebido no último período.
    - Os valores monetários não são arredondados durante os cálculos.
      O arredondamento ocorre somente na apresentação dos resultados.
    """

    # Limites utilizados na busca numérica da TIR.
    # A taxa mínima fica ligeiramente acima de -100%, pois taxas
    # inferiores ou iguais a -100% não são válidas para desconto.
    TIR_TAXA_MINIMA = -0.9999
    TIR_TAXA_MAXIMA = 1000.0
    TIR_PONTOS_BUSCA = 20000
    TIR_TOLERANCIA = 1e-7
    TIR_MAX_ITERACOES = 1000

    @staticmethod
    def _validar_numero(
        valor: Any,
        nome: str,
        minimo: Optional[float] = None,
        maximo: Optional[float] = None
    ) -> float:
        """
        Valida e converte um valor numérico.

        Rejeita:
        - Valores ausentes ou não numéricos;
        - Valores booleanos;
        - NaN e infinito;
        - Valores fora dos limites estabelecidos.
        """
        if isinstance(valor, bool):
            raise ValueError(
                "O campo '{}' deve ser numérico, não booleano.".format(nome)
            )

        try:
            numero = float(valor)
        except (TypeError, ValueError):
            raise ValueError(
                "O campo '{}' deve conter um número válido.".format(nome)
            )

        if not math.isfinite(numero):
            raise ValueError(
                "O campo '{}' não pode ser NaN ou infinito.".format(nome)
            )

        if minimo is not None and numero < minimo:
            raise ValueError(
                "O campo '{}' deve ser maior ou igual a {}.".format(
                    nome, minimo
                )
            )

        if maximo is not None and numero > maximo:
            raise ValueError(
                "O campo '{}' deve ser menor ou igual a {}.".format(
                    nome, maximo
                )
            )

        return numero

    @classmethod
    def _validar_entradas(cls, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida todos os dados de entrada e retorna uma estrutura
        normalizada para os cálculos.

        Esta etapa evita que valores inválidos sejam utilizados
        silenciosamente nos indicadores financeiros.
        """
        if not isinstance(dados, dict):
            raise ValueError("Os dados do projeto devem ser um objeto JSON.")

        if "tma" not in dados:
            raise ValueError("O campo obrigatório 'tma' não foi informado.")

        tma = cls._validar_numero(
            dados["tma"], "tma", minimo=-0.9999
        )

        aliquota = cls._validar_numero(
            dados.get("aliquota_imposto", 0.0),
            "aliquota_imposto",
            minimo=0.0,
            maximo=1.0
        )

        capex_inicial = cls._validar_numero(
            dados.get("capex_inicial", 0.0),
            "capex_inicial",
            minimo=0.0
        )

        capital_giro = cls._validar_numero(
            dados.get("capital_giro", 0.0),
            "capital_giro",
            minimo=0.0
        )

        valor_residual = cls._validar_numero(
            dados.get("valor_residual", 0.0),
            "valor_residual",
            minimo=0.0
        )

        periodos = dados.get("periodos")

        if not isinstance(periodos, list) or not periodos:
            raise ValueError(
                "O projeto deve possuir pelo menos um período de análise."
            )

        periodos_validados = []

        for indice, periodo in enumerate(periodos, start=1):
            if not isinstance(periodo, dict):
                raise ValueError(
                    "O período {} deve ser um objeto JSON.".format(indice)
                )

            receita = cls._validar_numero(
                periodo.get("receita_bruta", 0.0),
                "periodos[{}].receita_bruta".format(indice),
                minimo=0.0
            )

            opex = cls._validar_numero(
                periodo.get("opex", 0.0),
                "periodos[{}].opex".format(indice),
                minimo=0.0
            )

            capex_adicional = cls._validar_numero(
                periodo.get("capex_adicional", 0.0),
                "periodos[{}].capex_adicional".format(indice),
                minimo=0.0
            )

            periodos_validados.append({
                "receita_bruta": receita,
                "opex": opex,
                "capex_adicional": capex_adicional
            })

        return {
            "tma": tma,
            "aliquota_imposto": aliquota,
            "capex_inicial": capex_inicial,
            "capital_giro": capital_giro,
            "valor_residual": valor_residual,
            "periodos": periodos_validados,
            "unit_economics": dados.get("unit_economics")
        }

    @staticmethod
    def calcular_vpl(tma: float, fluxos: List[float]) -> float:
        """
        Calcula o Valor Presente Líquido.

        Fórmula:
            VPL = SOMA [ FCt / (1 + TMA)^t ]

        O primeiro elemento da lista representa FC0.
        """
        if tma <= -1:
            raise ValueError("A TMA deve ser superior a -100%.")

        return sum(
            fluxo / ((1.0 + tma) ** periodo)
            for periodo, fluxo in enumerate(fluxos)
        )

    @classmethod
    def _encontrar_raiz_tir(
        cls,
        fluxos: List[float],
        limite_inferior: float,
        limite_superior: float
    ) -> float:
        """
        Encontra uma raiz da função VPL utilizando bisseção.

        Os limites devem apresentar valores de VPL com sinais
        opostos ou um dos limites deve representar uma raiz.
        """
        inferior = limite_inferior
        superior = limite_superior

        vpl_inferior = cls.calcular_vpl(inferior, fluxos)
        vpl_superior = cls.calcular_vpl(superior, fluxos)

        if abs(vpl_inferior) < cls.TIR_TOLERANCIA:
            return inferior

        if abs(vpl_superior) < cls.TIR_TOLERANCIA:
            return superior

        if vpl_inferior * vpl_superior > 0:
            raise ValueError(
                "O intervalo informado não contém uma mudança de sinal."
            )

        for _ in range(cls.TIR_MAX_ITERACOES):
            meio = (inferior + superior) / 2.0
            vpl_meio = cls.calcular_vpl(meio, fluxos)

            if (
                abs(vpl_meio) < cls.TIR_TOLERANCIA
                or (superior - inferior) / 2.0 < cls.TIR_TOLERANCIA
            ):
                return meio

            if vpl_inferior * vpl_meio < 0:
                superior = meio
            else:
                inferior = meio
                vpl_inferior = vpl_meio

        return (inferior + superior) / 2.0

    @classmethod
    def calcular_tir(cls, fluxos: List[float]) -> Dict[str, Any]:
        """
        Procura soluções para a Taxa Interna de Retorno.

        A busca percorre uma faixa de taxas entre -99,99% e 100.000%,
        utilizando espaçamento uniforme em ln(1 + taxa).

        Isso permite uma busca mais equilibrada entre taxas negativas
        próximas de -100% e taxas positivas elevadas.

        Importante:
        A busca numérica é uma aproximação. Ela pode não identificar
        raízes múltiplas muito próximas ou raízes tangenciais, que
        não provocam mudança de sinal. Portanto, a ausência de raiz
        encontrada não prova matematicamente que nenhuma raiz exista.
        """
        if not fluxos:
            return {
                "taxas_encontradas": [],
                "status": "FLUXO_INSUFICIENTE"
            }

        possui_positivo = any(fluxo > 0 for fluxo in fluxos)
        possui_negativo = any(fluxo < 0 for fluxo in fluxos)

        if not (possui_positivo and possui_negativo):
            return {
                "taxas_encontradas": [],
                "status": "SEM_MUDANCA_DE_SINAL"
            }

        # A transformação logarítmica garante taxas sempre maiores
        # que -100% e distribui melhor os pontos de busca.
        x_minimo = math.log(1.0 + cls.TIR_TAXA_MINIMA)
        x_maximo = math.log(1.0 + cls.TIR_TAXA_MAXIMA)

        passo = (
            (x_maximo - x_minimo) / cls.TIR_PONTOS_BUSCA
        )

        taxas = []
        x_anterior = x_minimo
        taxa_anterior = math.exp(x_anterior) - 1.0
        vpl_anterior = cls.calcular_vpl(taxa_anterior, fluxos)

        for indice in range(1, cls.TIR_PONTOS_BUSCA + 1):
            x_atual = x_minimo + indice * passo
            taxa_atual = math.exp(x_atual) - 1.0
            vpl_atual = cls.calcular_vpl(taxa_atual, fluxos)

            if abs(vpl_anterior) < cls.TIR_TOLERANCIA:
                taxas.append(taxa_anterior)

            elif vpl_anterior * vpl_atual < 0:
                raiz = cls._encontrar_raiz_tir(
                    fluxos,
                    taxa_anterior,
                    taxa_atual
                )
                taxas.append(raiz)

            x_anterior = x_atual
            taxa_anterior = taxa_atual
            vpl_anterior = vpl_atual

        # Verifica também o último ponto da busca.
        if abs(vpl_anterior) < cls.TIR_TOLERANCIA:
            taxas.append(taxa_anterior)

        # Remove soluções duplicadas decorrentes da aproximação
        # numérica e da verificação dos limites dos intervalos.
        taxas_unicas = []

        for taxa in sorted(taxas):
            if not taxas_unicas or abs(
                taxa - taxas_unicas[-1]
            ) > 1e-5:
                taxas_unicas.append(taxa)

        if not taxas_unicas:
            status = "NENHUMA_RAIZ_ENCONTRADA_NO_INTERVALO"
        elif len(taxas_unicas) == 1:
            status = "SOLUCAO_UNICA_ENCONTRADA"
        else:
            status = "MULTIPLAS_SOLUCOES_ENCONTRADAS"

        return {
            "taxas_encontradas": taxas_unicas,
            "status": status
        }

    @staticmethod
    def calcular_payback(
        fluxos: List[float],
        tma: float = 0.0
    ) -> Optional[float]:
        """
        Calcula o Payback Simples ou Descontado.

        Com TMA igual a zero, calcula o Payback Simples.
        Com TMA diferente de zero, calcula o Payback Descontado.

        A interpolação linear estima a fração do período necessária
        para recuperar o investimento, pressupondo distribuição
        uniforme do fluxo dentro desse período.

        Retorna None se o saldo acumulado não se tornar positivo.
        """
        if tma <= -1:
            raise ValueError("A TMA deve ser superior a -100%.")

        if not fluxos:
            return None

        acumulado = 0.0

        for periodo, fluxo in enumerate(fluxos):
            fluxo_ajustado = fluxo / ((1.0 + tma) ** periodo)

            acumulado_anterior = acumulado
            acumulado += fluxo_ajustado

            if periodo == 0 and acumulado >= 0:
                return 0.0

            if periodo > 0 and acumulado >= 0:
                if fluxo_ajustado <= 0:
                    return float(periodo)

                fracao = (
                    -acumulado_anterior / fluxo_ajustado
                )

                return round(
                    (periodo - 1) + fracao,
                    2
                )

        return None

    @staticmethod
    def _calcular_indice_lucratividade(
        tma: float,
        beneficios: List[float],
        custos: List[float]
    ) -> Optional[float]:
        """
        Calcula o Índice de Lucratividade (IL).

        Definição adotada:
            IL = VP dos benefícios / VP dos custos e desembolsos

        Benefícios e custos são classificados separadamente antes do
        desconto, sem compensação entre componentes do mesmo período.

        Interpretação:
            IL > 1: valor presente dos benefícios superior aos custos.
            IL = 1: equilíbrio econômico.
            IL < 1: valor presente dos benefícios inferior aos custos.
        """
        if len(beneficios) != len(custos):
            raise ValueError(
                "As listas de benefícios e custos devem ter o mesmo tamanho."
            )

        valor_presente_beneficios = 0.0
        valor_presente_custos = 0.0

        for periodo, beneficio in enumerate(beneficios):
            fator_desconto = (1.0 + tma) ** periodo
            valor_presente_beneficios += beneficio / fator_desconto
            valor_presente_custos += custos[periodo] / fator_desconto

        if valor_presente_custos == 0:
            return None

        return valor_presente_beneficios / valor_presente_custos

    @classmethod
    def _calcular_unit_economics(
        cls,
        dados: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calcula indicadores simplificados de Unit Economics para SaaS.

        Premissas:
        - Ticket médio e custos são mensais.
        - A margem de contribuição é calculada por cliente.
        - O LTV utiliza churn mensal constante.
        - O LTV não considera desconto financeiro.
        - O CAC corresponde ao investimento mensal em marketing
          e vendas dividido pelos novos clientes do mesmo mês.
        """
        if not isinstance(dados, dict):
            raise ValueError("'unit_economics' deve ser um objeto JSON.")

        ticket = cls._validar_numero(
            dados.get("ticket_medio_mensal", 0.0),
            "unit_economics.ticket_medio_mensal",
            minimo=0.0
        )

        custo_variavel = cls._validar_numero(
            dados.get("custo_variavel_unitario", 0.0),
            "unit_economics.custo_variavel_unitario",
            minimo=0.0
        )

        custo_fixo = cls._validar_numero(
            dados.get("custo_fixo_mensal", 0.0),
            "unit_economics.custo_fixo_mensal",
            minimo=0.0
        )

        investimento_marketing = cls._validar_numero(
            dados.get("investimento_mkt_vendas_mensal", 0.0),
            "unit_economics.investimento_mkt_vendas_mensal",
            minimo=0.0
        )

        novos_clientes = cls._validar_numero(
            dados.get("novos_clientes_mes", 0.0),
            "unit_economics.novos_clientes_mes",
            minimo=0.0
        )

        churn = cls._validar_numero(
            dados.get("churn_mensal", 0.0),
            "unit_economics.churn_mensal",
            minimo=0.0,
            maximo=1.0
        )

        incluir_marketing = dados.get(
            "incluir_marketing_no_ponto_equilibrio",
            False
        )

        if not isinstance(incluir_marketing, bool):
            raise ValueError(
                "'incluir_marketing_no_ponto_equilibrio' "
                "deve ser verdadeiro ou falso."
            )

        margem_contribuicao = ticket - custo_variavel

        margem_percentual = (
            margem_contribuicao / ticket
            if ticket > 0 else 0.0
        )

        # Por padrão, o ponto de equilíbrio considera apenas os
        # custos fixos informados. O marketing pode ser incluído
        # explicitamente, evitando dupla contagem.
        base_ponto_equilibrio = custo_fixo

        if incluir_marketing:
            base_ponto_equilibrio += investimento_marketing

        ponto_equilibrio = (
            math.ceil(base_ponto_equilibrio / margem_contribuicao)
            if margem_contribuicao > 0
            else None
        )

        cac = (
            investimento_marketing / novos_clientes
            if novos_clientes > 0
            else None
        )

        # Quando o churn é zero, o LTV não é calculado como infinito.
        # O resultado fica indefinido até que exista uma hipótese
        # de retenção adequada.
        ltv = (
            (ticket * margem_percentual) / churn
            if churn > 0
            else None
        )

        ltv_cac = (
            ltv / cac
            if ltv is not None and cac is not None and cac > 0
            else None
        )

        return {
            "premissas": {
                "periodicidade": "MENSAL",
                "modelo_ltv": "MARGEM_DE_CONTRIBUICAO_DIVIDIDA_PELO_CHURN",
                "ltv_considera_desconto_financeiro": False,
                "marketing_incluido_no_ponto_equilibrio": incluir_marketing
            },
            "margem_contribuicao_unitaria": round(
                margem_contribuicao, 2
            ),
            "margem_contribuicao_pct": round(
                margem_percentual * 100, 2
            ),
            "ponto_equilibrio_clientes": ponto_equilibrio,
            "cac": round(cac, 2) if cac is not None else None,
            "ltv": round(ltv, 2) if ltv is not None else None,
            "relacao_ltv_cac": (
                round(ltv_cac, 2)
                if ltv_cac is not None else None
            )
        }

    @classmethod
    def analisar_projeto(
        cls,
        dados: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executa a análise econômica completa do projeto.

        Etapas:
        1. Valida e normaliza as entradas.
        2. Constrói o fluxo de caixa.
        3. Calcula os indicadores financeiros.
        4. Classifica a viabilidade pelo VPL.
        5. Calcula Unit Economics, quando informados.
        """
        entrada = cls._validar_entradas(dados)

        tma = entrada["tma"]
        aliquota = entrada["aliquota_imposto"]
        capex_inicial = entrada["capex_inicial"]
        capital_giro = entrada["capital_giro"]
        valor_residual = entrada["valor_residual"]
        periodos = entrada["periodos"]

        numero_periodos = len(periodos)

        # FC0 reúne o investimento inicial e a necessidade inicial
        # de capital de giro.
        fc0 = -(capex_inicial + capital_giro)

        fluxos_liquidos = [fc0]
        beneficios_por_periodo = [0.0]
        custos_por_periodo = [capex_inicial + capital_giro]
        if not math.isclose(
            beneficios_por_periodo[0] - custos_por_periodo[0],
            fluxos_liquidos[0],
            rel_tol=1e-12,
            abs_tol=1e-9,
        ):
            raise ArithmeticError(
                "A decomposição de benefícios e custos não corresponde "
                "ao fluxo líquido do período 0."
            )
        tabela_fluxo = []

        acumulado_simples = fc0
        acumulado_descontado = fc0

        tabela_fluxo.append({
            "periodo": 0,
            "receita_bruta": 0.0,
            "impostos": 0.0,
            "opex": 0.0,
            "capex_adicional": 0.0,
            "valor_residual": 0.0,
            "recuperacao_capital_giro": 0.0,
            "fluxo_liquido": round(fc0, 2),
            "fluxo_descontado": round(fc0, 2),
            "saldo_acumulado_simples": round(
                acumulado_simples, 2
            ),
            "saldo_acumulado_descontado": round(
                acumulado_descontado, 2
            )
        })

        for indice, periodo in enumerate(periodos, start=1):
            receita = periodo["receita_bruta"]
            opex = periodo["opex"]
            capex_adicional = periodo["capex_adicional"]

            # Simplificação tributária: a alíquota incide sobre
            # a receita bruta, e não sobre o lucro tributável.
            impostos = receita * aliquota

            # O capital de giro é recuperado integralmente somente
            # no encerramento do horizonte de análise.
            recuperacao_capital_giro = (
                capital_giro
                if indice == numero_periodos
                else 0.0
            )

            # O valor residual também é recebido no último período.
            recebimento_residual = (
                valor_residual
                if indice == numero_periodos
                else 0.0
            )

            fluxo_investimentos = (
                -capex_adicional
                + recuperacao_capital_giro
                + recebimento_residual
            )

            fluxo_liquido = (
                receita
                - impostos
                - opex
                + fluxo_investimentos
            )

            # Decomposição independente para o IL: receita líquida de
            # tributos, residual e recuperação são benefícios; OpEx e
            # CapEx adicional são custos. Os componentes não se compensam
            # antes de serem descontados.
            beneficios_periodo = (
                receita - impostos
                + recebimento_residual
                + recuperacao_capital_giro
            )
            custos_periodo = opex + capex_adicional

            if not math.isclose(
                beneficios_periodo - custos_periodo,
                fluxo_liquido,
                rel_tol=1e-12,
                abs_tol=1e-9,
            ):
                raise ArithmeticError(
                    "A decomposição de benefícios e custos não corresponde "
                    "ao fluxo líquido do período {}.".format(indice)
                )

            fluxo_descontado = (
                fluxo_liquido / ((1.0 + tma) ** indice)
            )

            fluxos_liquidos.append(fluxo_liquido)
            beneficios_por_periodo.append(beneficios_periodo)
            custos_por_periodo.append(custos_periodo)

            acumulado_simples += fluxo_liquido
            acumulado_descontado += fluxo_descontado

            tabela_fluxo.append({
                "periodo": indice,
                "receita_bruta": round(receita, 2),
                "impostos": round(impostos, 2),
                "opex": round(opex, 2),
                "capex_adicional": round(capex_adicional, 2),
                "valor_residual": round(
                    recebimento_residual, 2
                ),
                "recuperacao_capital_giro": round(
                    recuperacao_capital_giro, 2
                ),
                "fluxo_liquido": round(fluxo_liquido, 2),
                "fluxo_descontado": round(
                    fluxo_descontado, 2
                ),
                "saldo_acumulado_simples": round(
                    acumulado_simples, 2
                ),
                "saldo_acumulado_descontado": round(
                    acumulado_descontado, 2
                )
            })

        # Indicadores financeiros.
        vpl = cls.calcular_vpl(tma, fluxos_liquidos)
        resultado_tir = cls.calcular_tir(fluxos_liquidos)

        taxas_tir = resultado_tir["taxas_encontradas"]

        # Uma TIR única pode ser apresentada como indicador principal.
        # Quando existem múltiplas soluções, o campo principal fica
        # indefinido e todas as soluções encontradas são informadas.
        tir = taxas_tir[0] if len(taxas_tir) == 1 else None

        payback_simples = cls.calcular_payback(
            fluxos_liquidos,
            tma=0.0
        )

        payback_descontado = cls.calcular_payback(
            fluxos_liquidos,
            tma=tma
        )

        indice_lucratividade = cls._calcular_indice_lucratividade(
            tma,
            beneficios_por_periodo,
            custos_por_periodo
        )

        # A classificação principal considera o VPL.
        # A TIR é apresentada como indicador complementar.
        if vpl > 0:
            status_viabilidade = "VIAVEL"
            justificativa = (
                "VPL positivo: o projeto gera valor acima da TMA "
                "considerada, conforme as premissas informadas."
            )
        elif vpl < 0:
            status_viabilidade = "INVIAVEL"
            justificativa = (
                "VPL negativo: o projeto não remunera o capital "
                "à TMA considerada."
            )
        else:
            status_viabilidade = "INDIFERENTE"
            justificativa = (
                "VPL igual a zero: o projeto remunera exatamente "
                "a TMA considerada."
            )

        if resultado_tir["status"] == "MULTIPLAS_SOLUCOES_ENCONTRADAS":
            observacao_tir = (
                "Foram encontradas múltiplas TIRs. Não utilize uma "
                "única TIR como critério isolado de decisão."
            )
        elif resultado_tir["status"] == "NENHUMA_RAIZ_ENCONTRADA_NO_INTERVALO":
            observacao_tir = (
                "Nenhuma TIR foi encontrada no intervalo pesquisado. "
                "Isso não prova a inexistência de raízes fora do intervalo "
                "ou de raízes que não provoquem mudança de sinal."
            )
        elif resultado_tir["status"] == "SEM_MUDANCA_DE_SINAL":
            observacao_tir = (
                "O fluxo não apresenta entradas e saídas simultaneamente. "
                "A TIR não pode ser determinada por este procedimento."
            )
        else:
            observacao_tir = (
                "Foi encontrada uma solução para a TIR no intervalo "
                "numérico pesquisado."
            )

        if tir is not None:
            comparacao_tir = (
                "TIR superior à TMA."
                if tir > tma
                else "TIR igual ou inferior à TMA."
            )
        else:
            comparacao_tir = (
                "Não foi possível estabelecer uma comparação única "
                "entre TIR e TMA."
            )

        resultado = {
            "premissas_analise": {
                "tma_periodo_pct": round(tma * 100, 4),
                "aliquota_imposto_pct": round(aliquota * 100, 4),
                "modelo_tributario": (
                    "ALÍQUOTA SIMPLIFICADA SOBRE RECEITA BRUTA"
                ),
                "periodos_analisados": numero_periodos,
                "convencao_fluxo": "FIM DE CADA PERIODO",
                "capital_giro": (
                    "Investimento no período zero e recuperação "
                    "integral no último período."
                ),
                "valor_residual": (
                    "Recebimento integral no último período."
                ),
                "depreciacao_amortizacao": (
                    "Não modeladas neste cálculo."
                )
            },
            "indicadores_viabilidade": {
                "vpl": round(vpl, 2),
                "tir_periodo_pct": (
                    round(tir * 100, 4)
                    if tir is not None else None
                ),
                "tir_solucoes_encontradas_pct": [
                    round(taxa * 100, 4)
                    for taxa in taxas_tir
                ],
                "tir_status": resultado_tir["status"],
                "tir_interpretacao": observacao_tir,
                "comparacao_tir_tma": comparacao_tir,
                "payback_simples_periodos": payback_simples,
                "payback_descontado_periodos": payback_descontado,
                "indice_lucratividade": (
                    round(indice_lucratividade, 4)
                    if indice_lucratividade is not None
                    else None
                ),
                "status_viabilidade": status_viabilidade,
                "justificativa_viabilidade": justificativa
            },
            "fluxo_de_caixa": tabela_fluxo
        }

        # Unit Economics é opcional e só é calculado quando informado.
        dados_saas = entrada["unit_economics"]

        if dados_saas is not None:
            resultado["unit_economics_saas"] = (
                cls._calcular_unit_economics(dados_saas)
            )

        return resultado


def main() -> None:
    """
    Interface de linha de comando.

    Aceita dados por:
    - Argumento --json;
    - Arquivo informado em --file;
    - Entrada padrão (stdin).

    Os argumentos --json e --file são mutuamente exclusivos.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Calculadora de Engenharia Econômica para projetos "
            "de software: VPL, TIR, Payback e Unit Economics."
        )
    )

    grupo_entrada = parser.add_mutually_exclusive_group()

    grupo_entrada.add_argument(
        "--json",
        type=str,
        help="String JSON com os dados do projeto."
    )

    grupo_entrada.add_argument(
        "--file",
        type=str,
        help="Caminho para arquivo JSON com os dados do projeto."
    )

    args = parser.parse_args()

    try:
        if args.file:
            with open(args.file, "r", encoding="utf-8") as arquivo:
                payload = json.load(arquivo)

        elif args.json:
            payload = json.loads(args.json)

        else:
            payload = json.load(sys.stdin)

        resultado = CalculadoraEngenhariaEconomica.analisar_projeto(
            payload
        )

        print(
            json.dumps(
                resultado,
                indent=2,
                ensure_ascii=False,
                allow_nan=False
            )
        )

    except (ValueError, TypeError, KeyError, OverflowError) as erro:
        print(
            json.dumps(
                {"erro": str(erro)},
                ensure_ascii=False
            ),
            file=sys.stderr
        )
        sys.exit(1)

    except OSError as erro:
        print(
            json.dumps(
                {"erro": "Erro ao acessar arquivo: {}".format(erro)},
                ensure_ascii=False
            ),
            file=sys.stderr
        )
        sys.exit(1)

    except json.JSONDecodeError as erro:
        print(
            json.dumps(
                {"erro": "JSON inválido: {}".format(erro)},
                ensure_ascii=False
            ),
            file=sys.stderr
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
