#!/usr/bin/env python3
"""
Calculadora Determinística de Engenharia Econômica para Projetos de Software.
Calcula: Fluxo de Caixa Líquido, VPL (NPV), TIR (IRR), Payback Simples,
Payback Descontado, Ponto de Equilíbrio e Unit Economics (CAC/LTV).
Compatível com Python 3.8+ (apenas biblioteca padrão).
"""

import argparse
import json
import math
import sys
from typing import Any, Dict, List, Optional


def calcular_vpl(tma: float, fluxos: List[float]) -> float:
    """Calcula o Valor Presente Líquido dado uma TMA por período e lista de fluxos [FC0, FC1, ...]."""
    return sum(fc / ((1.0 + tma) ** t) for t, fc in enumerate(fluxos))


def calcular_tir(fluxos: List[float], tol: float = 1e-7, max_iter: int = 1000) -> Optional[float]:
    """
    Calcula a Taxa Interna de Retorno (TIR) via método da Bisseção com varredura de intervalo.
    Retorna None caso não exista mudança de sinal ou raiz real no intervalo [-0.99, 10.0].
    """
    if not fluxos or all(f >= 0 for f in fluxos) or all(f <= 0 for f in fluxos):
        return None

    low, high = -0.99, 10.0
    f_low = calcular_vpl(low, fluxos)
    f_high = calcular_vpl(high, fluxos)

    if f_low * f_high > 0:
        step = 0.01
        r = -0.99
        found = False
        while r < 10.0:
            if calcular_vpl(r, fluxos) * calcular_vpl(r + step, fluxos) <= 0:
                low, high = r, r + step
                found = True
                break
            r += step
        if not found:
            return None

    mid = 0.0
    for _ in range(max_iter):
        mid = (low + high) / 2.0
        f_mid = calcular_vpl(mid, fluxos)
        if abs(f_mid) < tol or (high - low) / 2.0 < tol:
            return mid
        if calcular_vpl(low, fluxos) * f_mid <= 0:
            high = mid
        else:
            low = mid
    return mid


def calcular_payback(fluxos: List[float], tma: float = 0.0) -> Optional[float]:
    """
    Calcula o Payback Simples (tma=0) ou Payback Descontado (tma>0) com interpolação linear.
    Retorna o número de períodos até o saldo acumulado tornar-se >= 0, ou None se não recuperar.
    """
    acumulado = 0.0
    for t, fc in enumerate(fluxos):
        fc_ajustado = fc / ((1.0 + tma) ** t)
        acumulado_anterior = acumulado
        acumulado += fc_ajustado
        if t > 0 and acumulado >= 0.0:
            if fc_ajustado == 0:
                return float(t)
            fracao = abs(acumulado_anterior) / fc_ajustado
            return round((t - 1) + fracao, 2)
    return None


def analisar_projeto(dados: Dict[str, Any]) -> Dict[str, Any]:
    """Executa a modelagem financeira completa do projeto de software."""
    tma = float(dados["tma"])
    aliquota_imposto = float(dados.get("aliquota_imposto", 0.0))
    capex_inicial = float(dados.get("capex_inicial", 0.0))
    capital_giro = float(dados.get("capital_giro", 0.0))
    valor_residual = float(dados.get("valor_residual", 0.0))

    periodos = dados.get("periodos", [])
    tabela_fluxo = []

    fc0 = -(capex_inicial + capital_giro)
    fluxos_liquidos = [fc0]
    acumulado_simples = fc0
    acumulado_descontado = fc0

    tabela_fluxo.append({
        "periodo": 0,
        "receita_bruta": 0.0,
        "impostos": 0.0,
        "opex": 0.0,
        "capex_giro_vr": round(fc0, 2),
        "fluxo_liquido": round(fc0, 2),
        "fluxo_descontado": round(fc0, 2),
        "saldo_acumulado_simples": round(acumulado_simples, 2),
        "saldo_acumulado_descontado": round(acumulado_descontado, 2),
    })

    n = len(periodos)
    for idx, p in enumerate(periodos, start=1):
        receita = float(p.get("receita_bruta", 0.0))
        opex = float(p.get("opex", 0.0))
        capex_extra = float(p.get("capex_adicional", 0.0))
        impostos = receita * aliquota_imposto

        retorno_final = (valor_residual + capital_giro) if idx == n else 0.0
        investimento_liquido_periodo = retorno_final - capex_extra

        fc_t = (receita - impostos - opex) + investimento_liquido_periodo
        fc_desc_t = fc_t / ((1.0 + tma) ** idx)

        fluxos_liquidos.append(fc_t)
        acumulado_simples += fc_t
        acumulado_descontado += fc_desc_t

        tabela_fluxo.append({
            "periodo": idx,
            "receita_bruta": round(receita, 2),
            "impostos": round(impostos, 2),
            "opex": round(opex, 2),
            "capex_giro_vr": round(investimento_liquido_periodo, 2),
            "fluxo_liquido": round(fc_t, 2),
            "fluxo_descontado": round(fc_desc_t, 2),
            "saldo_acumulado_simples": round(acumulado_simples, 2),
            "saldo_acumulado_descontado": round(acumulado_descontado, 2),
        })

    vpl = calcular_vpl(tma, fluxos_liquidos)
    tir = calcular_tir(fluxos_liquidos)
    pb_simples = calcular_payback(fluxos_liquidos, tma=0.0)
    pb_descontado = calcular_payback(fluxos_liquidos, tma=tma)

    investimento_total_vp = abs(fc0) + sum(
        float(p.get("capex_adicional", 0.0)) / ((1.0 + tma) ** idx)
        for idx, p in enumerate(periodos, start=1)
    )
    il = ((vpl + investimento_total_vp) / investimento_total_vp) if investimento_total_vp > 0 else None

    resultado: Dict[str, Any] = {
        "indicadores_viabilidade": {
            "tma_periodo_pct": round(tma * 100, 4),
            "vpl": round(vpl, 2),
            "tir_periodo_pct": round(tir * 100, 4) if tir is not None else None,
            "payback_simples_periodos": pb_simples,
            "payback_descontado_periodos": pb_descontado,
            "indice_lucratividade": round(il, 4) if il is not None else None,
            "status_viabilidade": "VIAVEL (VPL > 0 e TIR > TMA)" if (vpl > 0 and (tir is not None and tir > tma)) else "INVIAVEL OU REQUER REVISAO",
        },
        "fluxo_de_caixa": tabela_fluxo,
    }

    saas = dados.get("unit_economics")
    if saas:
        ticket = float(saas.get("ticket_medio_mensal", 0.0))
        custo_var_unit = float(saas.get("custo_variavel_unitario", 0.0))
        custo_fixo_mensal = float(saas.get("custo_fixo_mensal", 0.0))
        inv_mkt_vendas = float(saas.get("investimento_mkt_vendas_mensal", 0.0))
        novos_clientes = float(saas.get("novos_clientes_mes", 0.0))
        churn = float(saas.get("churn_mensal", 0.0))

        margem_contrib = ticket - custo_var_unit
        margem_pct = (margem_contrib / ticket) if ticket > 0 else 0.0
        break_even_clientes = math.ceil(custo_fixo_mensal / margem_contrib) if margem_contrib > 0 else None
        cac = (inv_mkt_vendas / novos_clientes) if novos_clientes > 0 else None
        ltv = ((ticket * margem_pct) / churn) if churn > 0 else None
        ltv_cac = (ltv / cac) if (ltv is not None and cac and cac > 0) else None

        resultado["unit_economics_saas"] = {
            "margem_contribuicao_unitaria": round(margem_contrib, 2),
            "margem_contribuicao_pct": round(margem_pct * 100, 2),
            "ponto_equilibrio_clientes": break_even_clientes,
            "cac": round(cac, 2) if cac is not None else None,
            "ltv": round(ltv, 2) if ltv is not None else None,
            "relacao_ltv_cac": round(ltv_cac, 2) if ltv_cac is not None else None,
        }

    return resultado


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cálculo determinístico de VPL, TIR, Payback e Unit Economics para Software."
    )
    parser.add_argument("--json", type=str, help="String JSON com os dados do projeto.")
    parser.add_argument("--file", type=str, help="Caminho para arquivo JSON com os dados do projeto.")
    args = parser.parse_args()

    try:
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                payload = json.load(f)
        elif args.json:
            payload = json.loads(args.json)
        else:
            payload = json.load(sys.stdin)

        resultado = analisar_projeto(payload)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"erro": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()