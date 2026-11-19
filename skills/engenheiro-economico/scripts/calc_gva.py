#!/usr/bin/env python3
"""
Calculadora Determinística de Gerenciamento de Valor Agregado (GVA / EVM) Ágil
e Priorização Econômica de Backlog (Valor vs. Esforço).
Compatível com Python 3.8+ (apenas biblioteca padrão).
"""

import argparse
import json
import sys
from typing import Any, Dict, List


def calcular_gva_agil(gva: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula indicadores de GVA adaptados ao desenvolvimento ágil com Story Points:
    - VSP: Valor por Story Point (BAC / Total_SP_Planejado)
    - VPA (PV): Valor Planejado Acumulado até a sprint atual
    - VAG (EV): Valor Agregado Acumulado (SP entregues * VSP)
    - CR (AC): Custo Real Acumulado (Horas trabalhadas * Custo/hora ou custo direto informado)
    - IDC (CPI) e IDP (SPI)
    - EAC (Estimativa no Término) e ETC (Estimativa para Terminar)
    """
    bac = float(gva["orcamento_total_bac"])
    total_sp_projeto = float(gva["total_sp_projeto"])
    sp_planejados_ate_agora = float(gva["sp_planejados_ate_agora"])
    sp_entregues_ate_agora = float(gva["sp_entregues_ate_agora"])

    if "custo_real_acumulado" in gva:
        cr = float(gva["custo_real_acumulado"])
    else:
        horas = float(gva["horas_trabalhadas"])
        custo_hora = float(gva["custo_hora"])
        cr = horas * custo_hora

    vsp = bac / total_sp_projeto if total_sp_projeto > 0 else 0.0
    vpa = sp_planejados_ate_agora * vsp
    vag = sp_entregues_ate_agora * vsp

    variacao_custo_vc = vag - cr
    variacao_prazo_vpz = vag - vpa

    idc = (vag / cr) if cr > 0 else 0.0
    idp = (vag / vpa) if vpa > 0 else 0.0

    eac = (bac / idc) if idc > 0 else None
    etc = (eac - cr) if eac is not None else None
    vac = (bac - eac) if eac is not None else None

    status_custo = "Abaixo do orçamento (Eficiente)" if idc >= 1.0 else "Acima do orçamento (Estouro)"
    status_prazo = "Adiantado ou no prazo" if idp >= 1.0 else "Atrasado em relação ao cronograma"

    return {
        "parametros_base": {
            "orcamento_total_bac": round(bac, 2),
            "total_sp_projeto": total_sp_projeto,
            "valor_por_story_point_vsp": round(vsp, 2),
        },
        "metricas_evm": {
            "vpa_valor_planejado": round(vpa, 2),
            "vag_valor_agregado": round(vag, 2),
            "cr_custo_real": round(cr, 2),
            "vc_variacao_custo": round(variacao_custo_vc, 2),
            "vpz_variacao_prazo": round(variacao_prazo_vpz, 2),
            "idc_cpi": round(idc, 4),
            "idp_spi": round(idp, 4),
        },
        "projecoes_termino": {
            "eac_estimativa_no_termino": round(eac, 2) if eac is not None else None,
            "etc_estimativa_para_terminar": round(etc, 2) if etc is not None else None,
            "vac_variacao_no_termino": round(vac, 2) if vac is not None else None,
            "diagnostico_custo": status_custo,
            "diagnostico_prazo": status_prazo,
        },
    }


def priorizar_backlog(itens: List[Dict[str, Any]], pesos: Dict[str, float]) -> List[Dict[str, Any]]:
    """
    Prioriza funcionalidades pela matriz econômica (escala 1 a 5, onde 5 = melhor cenário).
    """
    w_v = float(pesos.get("valor", 0.40))
    w_c = float(pesos.get("custo", 0.20))
    w_e = float(pesos.get("esforco", 0.25))
    w_r = float(pesos.get("risco", 0.15))

    ranking = []
    for item in itens:
        v = float(item["valor"])
        c = float(item["custo"])
        e = float(item["esforco"])
        r = float(item["risco"])
        score = (w_v * v) + (w_c * c) + (w_e * e) + (w_r * r)
        ranking.append({
            "id": item.get("id", ""),
            "funcionalidade": item["nome"],
            "valor": v,
            "custo_nota": c,
            "esforco_nota": e,
            "risco_nota": r,
            "score_economico": round(score, 3),
        })

    ranking.sort(key=lambda x: x["score_economico"], reverse=True)
    for pos, r_item in enumerate(ranking, start=1):
        r_item["prioridade_rank"] = pos
    return ranking


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cálculo determinístico de GVA/EVM Ágil e Priorização Econômica de Backlog."
    )
    parser.add_argument("--json", type=str, help="String JSON com dados de 'gva' e/ou 'backlog'.")
    parser.add_argument("--file", type=str, help="Caminho para arquivo JSON.")
    args = parser.parse_args()

    try:
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                payload = json.load(f)
        elif args.json:
            payload = json.loads(args.json)
        else:
            payload = json.load(sys.stdin)

        saida: Dict[str, Any] = {}
        if "gva" in payload:
            saida["gva_agil"] = calcular_gva_agil(payload["gva"])
        if "backlog" in payload:
            pesos = payload.get("pesos_priorizacao", {"valor": 0.40, "custo": 0.20, "esforco": 0.25, "risco": 0.15})
            saida["priorizacao_backlog"] = priorizar_backlog(payload["backlog"], pesos)

        print(json.dumps(saida, indent=2, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"erro": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()