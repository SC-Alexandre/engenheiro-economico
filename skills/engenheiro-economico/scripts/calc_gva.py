#!/usr/bin/env python3
"""
Calculadora de Engenharia Econômica para Projetos de Software.

Funcionalidades:
1. Gerenciamento de Valor Agregado (GVA / EVM) adaptado a sprints ágeis.
2. Projeções de custo no término do projeto (EAC, ETC e VAC).
3. Priorização econômica de backlog por benefícios versus esforço.

Compatibilidade: Python 3.8+
Dependências: somente biblioteca padrão.

IMPORTANTE:
- Story Points são medidas relativas de esforço e complexidade.
- A conversão de Story Points em valor monetário é uma aproximação
  gerencial para distribuir o orçamento do projeto.
- O ranking do backlog é um modelo multicritério de apoio à decisão.
- Os resultados dependem da qualidade das premissas informadas.
"""

import argparse
import json
import math
import sys
from typing import Any, Dict, List, Optional


class CalculadoraGVA:
    """
    Centraliza os cálculos de GVA/EVM e a priorização econômica do backlog.

    Os métodos são estáticos porque os cálculos não dependem do estado
    interno de uma instância da classe.
    """

    # Métodos disponíveis para estimar o custo final do projeto.
    METODOS_EAC = (
        "desempenho_custo",
        "orcamento_restante",
        "desempenho_combinado",
    )

    # Pesos padrão dos critérios de benefício.
    PESOS_BENEFICIOS_PADRAO = {
        "valor": 0.60,
        "alinhamento_estrategico": 0.25,
        "reducao_risco": 0.15,
    }

    # Pesos padrão dos critérios de sacrifício.
    PESOS_ESFORCO_PADRAO = {
        "esforco": 0.70,
        "custo": 0.30,
    }

    # ---------------------------------------------------------
    # VALIDAÇÕES GERAIS
    # ---------------------------------------------------------

    @staticmethod
    def _validar_objeto(dados: Any, nome: str) -> Dict[str, Any]:
        """Garante que a entrada seja um objeto/dicionário JSON."""
        if not isinstance(dados, dict):
            raise ValueError(
                "O campo '{}' deve ser um objeto JSON.".format(nome)
            )
        return dados

    @staticmethod
    def _validar_numero(
        valor: Any,
        nome: str,
        minimo: Optional[float] = None,
        maximo: Optional[float] = None,
    ) -> float:
        """
        Converte e valida um número.

        Rejeita:
        - Booleanos, mesmo que Python os interprete como inteiros.
        - Textos não numéricos.
        - Valores NaN e infinitos.
        - Valores fora dos limites definidos.
        """
        if isinstance(valor, bool):
            raise ValueError(
                "O campo '{}' deve ser numérico.".format(nome)
            )

        try:
            numero = float(valor)
        except (TypeError, ValueError):
            raise ValueError(
                "O campo '{}' deve ser numérico.".format(nome)
            )

        if not math.isfinite(numero):
            raise ValueError(
                "O campo '{}' deve possuir um valor finito.".format(nome)
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

    @staticmethod
    def _validar_campo_obrigatorio(
        dados: Dict[str, Any],
        campo: str,
        contexto: str,
    ) -> Any:
        """Verifica se um campo obrigatório está presente."""
        if campo not in dados:
            raise ValueError(
                "Campo obrigatório ausente: '{}.{}'.".format(
                    contexto, campo
                )
            )
        return dados[campo]

    # ---------------------------------------------------------
    # GERENCIAMENTO DE VALOR AGREGADO (GVA / EVM)
    # ---------------------------------------------------------

    @staticmethod
    def calcular_gva(gva: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula indicadores de GVA/EVM para um projeto de software.

        Estrutura esperada:

        {
            "orcamento_total_bac": 100000,
            "total_sp_projeto": 500,
            "sp_planejados_ate_agora": 200,
            "sp_entregues_ate_agora": 180,
            "custo_real_acumulado": 42000,
            "metodo_eac": "desempenho_custo"
        }

        Alternativamente, o custo real pode ser calculado com:
        - horas_trabalhadas
        - custo_hora

        Os Story Points são convertidos proporcionalmente ao BAC.
        """

        gva = CalculadoraGVA._validar_objeto(gva, "gva")

        # 1. Validar orçamento total do projeto (BAC).
        bac = CalculadoraGVA._validar_numero(
            CalculadoraGVA._validar_campo_obrigatorio(
                gva, "orcamento_total_bac", "gva"
            ),
            "orcamento_total_bac",
            minimo=0.01,
        )

        # 2. Validar o total de Story Points do projeto.
        total_sp = CalculadoraGVA._validar_numero(
            CalculadoraGVA._validar_campo_obrigatorio(
                gva, "total_sp_projeto", "gva"
            ),
            "total_sp_projeto",
            minimo=0.01,
        )

        # 3. Validar o planejamento acumulado até a sprint atual.
        sp_planejados = CalculadoraGVA._validar_numero(
            CalculadoraGVA._validar_campo_obrigatorio(
                gva, "sp_planejados_ate_agora", "gva"
            ),
            "sp_planejados_ate_agora",
            minimo=0.0,
            maximo=total_sp,
        )

        # 4. Validar os Story Points efetivamente entregues.
        #
        # É permitido entregar mais SP do que o planejado até a sprint
        # atual: isso pode representar adiantamento do cronograma.
        # O limite é o total de SP previsto para o projeto.
        sp_entregues = CalculadoraGVA._validar_numero(
            CalculadoraGVA._validar_campo_obrigatorio(
                gva, "sp_entregues_ate_agora", "gva"
            ),
            "sp_entregues_ate_agora",
            minimo=0.0,
            maximo=total_sp,
        )

        # 5. Determinar o custo real acumulado (CR / AC).
        #
        # Se o custo acumulado for informado diretamente, ele tem
        # prioridade sobre o cálculo por horas trabalhadas.
        if "custo_real_acumulado" in gva:
            cr = CalculadoraGVA._validar_numero(
                gva["custo_real_acumulado"],
                "custo_real_acumulado",
                minimo=0.0,
            )
            origem_cr = "CUSTO REAL INFORMADO DIRETAMENTE"
        else:
            horas = CalculadoraGVA._validar_numero(
                CalculadoraGVA._validar_campo_obrigatorio(
                    gva, "horas_trabalhadas", "gva"
                ),
                "horas_trabalhadas",
                minimo=0.0,
            )

            custo_hora = CalculadoraGVA._validar_numero(
                CalculadoraGVA._validar_campo_obrigatorio(
                    gva, "custo_hora", "gva"
                ),
                "custo_hora",
                minimo=0.0,
            )

            cr = horas * custo_hora
            origem_cr = "HORAS TRABALHADAS X CUSTO POR HORA"

        if not math.isfinite(cr):
            raise ValueError(
                "O custo real calculado ultrapassou o limite numérico."
            )

        # 6. Validar o método de projeção do custo final.
        metodo_eac = gva.get("metodo_eac", "desempenho_custo")

        if metodo_eac not in CalculadoraGVA.METODOS_EAC:
            raise ValueError(
                "Método EAC inválido. Utilize: {}.".format(
                    ", ".join(CalculadoraGVA.METODOS_EAC)
                )
            )

        # 7. Calcular o valor monetário proporcional por Story Point.
        #
        # Premissa simplificadora:
        # O orçamento total é distribuído proporcionalmente aos SP.
        vsp = bac / total_sp

        # 8. Calcular os indicadores básicos do GVA.
        vpa = sp_planejados * vsp
        vag = sp_entregues * vsp

        # Variação de custo: positivo indica desempenho favorável.
        vc = vag - cr

        # Variação de prazo: positivo indica adiantamento.
        vpz = vag - vpa

        # 9. Calcular IDC (CPI).
        #
        # Quando CR = 0, não existe base de comparação para o índice.
        # Se CR > 0 e VAG = 0, o IDC é efetivamente zero.
        idc = vag / cr if cr > 0 else None

        # 10. Calcular IDP (SPI).
        #
        # Quando VPA = 0, não existe valor planejado para comparação.
        # Se VPA > 0 e VAG = 0, o IDP é efetivamente zero.
        idp = vag / vpa if vpa > 0 else None

        # 11. Projetar o custo no término (EAC).
        #
        # Método 1: desempenho de custo constante.
        # EAC = BAC / IDC
        #
        # Método 2: execução do trabalho restante conforme orçamento.
        # EAC = CR + (BAC - VAG)
        #
        # Método 3: desempenho combinado de custo e prazo.
        # EAC = CR + (BAC - VAG) / (IDC * IDP)
        #
        # O EAC pode ser indefinido quando não há dados suficientes
        # para sustentar matematicamente a projeção.
        if metodo_eac == "desempenho_custo":
            eac = bac / idc if idc is not None and idc > 0 else None

        elif metodo_eac == "orcamento_restante":
            eac = cr + (bac - vag)

        else:
            denominador = (
                idc * idp
                if idc is not None and idp is not None
                else None
            )

            eac = (
                cr + (bac - vag) / denominador
                if denominador is not None and denominador > 0
                else None
            )

        # 12. Calcular indicadores derivados da projeção.
        if eac is not None:
            etc = eac - cr
            vac = bac - eac
        else:
            etc = None
            vac = None

        # 13. Diagnosticar desempenho de custo.
        if idc is None:
            diagnostico_custo = (
                "INDEFINIDO: custo real igual a zero."
            )
        elif idc >= 1.0:
            diagnostico_custo = (
                "FAVORAVEL: desempenho de custo igual ou superior ao planejado."
            )
        else:
            diagnostico_custo = (
                "DESFAVORAVEL: custo real superior ao valor agregado."
            )

        # 14. Diagnosticar desempenho de prazo.
        if idp is None:
            diagnostico_prazo = (
                "INDEFINIDO: não existe valor planejado acumulado."
            )
        elif idp >= 1.0:
            diagnostico_prazo = (
                "FAVORAVEL: desempenho igual ou superior ao planejamento."
            )
        else:
            diagnostico_prazo = (
                "DESFAVORAVEL: entrega inferior ao planejamento."
            )

        # 15. Diagnosticar a projeção de custo.
        if eac is None:
            diagnostico_eac = (
                "PROJECAO INDEFINIDA: dados insuficientes para o método escolhido."
            )
        elif vac >= 0:
            diagnostico_eac = (
                "PROJECAO FAVORAVEL: custo final estimado dentro do BAC."
            )
        else:
            diagnostico_eac = (
                "PROJECAO DESFAVORAVEL: custo final estimado acima do BAC."
            )

        # 16. Montar resultado organizado para consumo por outras ferramentas.
        return {
            "premissas": {
                "modelo": "GVA/EVM ADAPTADO A STORY POINTS",
                "orcamento_total_bac": round(bac, 2),
                "total_sp_projeto": round(total_sp, 2),
                "valor_por_story_point": round(vsp, 2),
                "origem_custo_real": origem_cr,
                "metodo_eac": metodo_eac,
                "observacao": (
                    "A conversao de Story Points em valor monetario "
                    "e uma aproximacao proporcional do BAC."
                ),
            },
            "progresso": {
                "sp_planejados_acumulados": round(sp_planejados, 2),
                "sp_entregues_acumulados": round(sp_entregues, 2),
                "percentual_planejado": round(
                    (sp_planejados / total_sp) * 100, 2
                ),
                "percentual_entregue": round(
                    (sp_entregues / total_sp) * 100, 2
                ),
            },
            "metricas_evm": {
                "vpa_valor_planejado": round(vpa, 2),
                "vag_valor_agregado": round(vag, 2),
                "cr_custo_real": round(cr, 2),
                "vc_variacao_custo": round(vc, 2),
                "vpz_variacao_prazo": round(vpz, 2),
                "idc_cpi": round(idc, 4) if idc is not None else None,
                "idp_spi": round(idp, 4) if idp is not None else None,
            },
            "projecoes_termino": {
                "eac_estimativa_no_termino": (
                    round(eac, 2) if eac is not None else None
                ),
                "etc_estimativa_para_terminar": (
                    round(etc, 2) if etc is not None else None
                ),
                "vac_variacao_no_termino": (
                    round(vac, 2) if vac is not None else None
                ),
                "diagnostico_eac": diagnostico_eac,
            },
            "diagnosticos": {
                "desempenho_custo": diagnostico_custo,
                "desempenho_prazo": diagnostico_prazo,
            },
        }

    # ---------------------------------------------------------
    # PRIORIZAÇÃO ECONÔMICA DO BACKLOG
    # ---------------------------------------------------------

    @staticmethod
    def _validar_pesos(
        pesos: Any,
        pesos_padrao: Dict[str, float],
        nome_grupo: str,
    ) -> Dict[str, float]:
        """
        Valida e normaliza os pesos de um grupo de critérios.

        A soma dos pesos não precisa ser exatamente 1.
        Os pesos informados são normalizados proporcionalmente.

        Isso permite, por exemplo, informar 60, 25 e 15
        em vez de 0.60, 0.25 e 0.15.
        """
        if pesos is None:
            pesos = pesos_padrao

        pesos = CalculadoraGVA._validar_objeto(
            pesos, "pesos_{}".format(nome_grupo)
        )

        if set(pesos.keys()) != set(pesos_padrao.keys()):
            raise ValueError(
                "Os pesos de '{}' devem conter exatamente: {}.".format(
                    nome_grupo,
                    ", ".join(pesos_padrao.keys()),
                )
            )

        pesos_validados = {}

        for criterio in pesos_padrao:
            pesos_validados[criterio] = (
                CalculadoraGVA._validar_numero(
                    pesos[criterio],
                    "pesos_{}.{}".format(nome_grupo, criterio),
                    minimo=0.0,
                )
            )

        soma = sum(pesos_validados.values())

        if soma <= 0:
            raise ValueError(
                "A soma dos pesos de '{}' deve ser maior que zero.".format(
                    nome_grupo
                )
            )

        # Normalização: a soma dos pesos resultantes será igual a 1.
        return {
            criterio: peso / soma
            for criterio, peso in pesos_validados.items()
        }

    @staticmethod
    def priorizar_backlog(
        itens: List[Dict[str, Any]],
        pesos: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Calcula um ranking econômico de funcionalidades.

        Cada item deve informar:

        {
            "id": "RF01",
            "nome": "Modulo de pagamentos",
            "valor": 5,
            "alinhamento_estrategico": 4,
            "reducao_risco": 3,
            "esforco": 2,
            "custo": 3
        }

        Escala de notas: 1 a 5.

        BENEFÍCIOS:
        - valor: 5 representa maior valor de negócio;
        - alinhamento_estrategico: 5 representa maior alinhamento;
        - reducao_risco: 5 representa maior redução de risco.

        SACRIFÍCIOS:
        - esforco: 5 representa maior esforço;
        - custo: 5 representa maior custo.

        Fórmula:

        Benefício ponderado =
            soma dos critérios de benefício * seus pesos.

        Esforço ponderado =
            soma dos critérios de sacrifício * seus pesos.

        Índice de prioridade =
            benefício ponderado / esforço ponderado.

        Quanto maior o índice, maior a relação entre benefício
        estimado e sacrifício necessário.
        """

        if not isinstance(itens, list):
            raise ValueError(
                "O campo 'backlog' deve ser uma lista."
            )

        if not itens:
            raise ValueError(
                "O backlog deve possuir pelo menos um item."
            )

        pesos = pesos or {}

        if not isinstance(pesos, dict):
            raise ValueError(
                "O campo 'pesos_priorizacao' deve ser um objeto."
            )

        pesos_beneficios = CalculadoraGVA._validar_pesos(
            pesos.get("beneficios"),
            CalculadoraGVA.PESOS_BENEFICIOS_PADRAO,
            "beneficios",
        )

        pesos_esforco = CalculadoraGVA._validar_pesos(
            pesos.get("esforco"),
            CalculadoraGVA.PESOS_ESFORCO_PADRAO,
            "esforco",
        )

        ranking = []

        for indice, item in enumerate(itens):
            item = CalculadoraGVA._validar_objeto(
                item, "backlog[{}]".format(indice)
            )

            # O nome identifica a funcionalidade no relatório.
            nome = item.get("nome")

            if not isinstance(nome, str) or not nome.strip():
                raise ValueError(
                    "O item backlog[{}] deve possuir um nome válido.".format(
                        indice
                    )
                )

            # Todas as notas devem estar entre 1 e 5.
            valor = CalculadoraGVA._validar_numero(
                item.get("valor"),
                "backlog[{}].valor".format(indice),
                minimo=1,
                maximo=5,
            )

            alinhamento = CalculadoraGVA._validar_numero(
                item.get("alinhamento_estrategico"),
                "backlog[{}].alinhamento_estrategico".format(indice),
                minimo=1,
                maximo=5,
            )

            reducao_risco = CalculadoraGVA._validar_numero(
                item.get("reducao_risco"),
                "backlog[{}].reducao_risco".format(indice),
                minimo=1,
                maximo=5,
            )

            esforco = CalculadoraGVA._validar_numero(
                item.get("esforco"),
                "backlog[{}].esforco".format(indice),
                minimo=1,
                maximo=5,
            )

            custo = CalculadoraGVA._validar_numero(
                item.get("custo"),
                "backlog[{}].custo".format(indice),
                minimo=1,
                maximo=5,
            )

            # Benefício agregado: notas maiores representam condições
            # mais favoráveis.
            beneficio = (
                pesos_beneficios["valor"] * valor
                + pesos_beneficios["alinhamento_estrategico"] * alinhamento
                + pesos_beneficios["reducao_risco"] * reducao_risco
            )

            # Sacrifício agregado: notas maiores representam maior
            # esforço ou custo.
            sacrificio = (
                pesos_esforco["esforco"] * esforco
                + pesos_esforco["custo"] * custo
            )

            # Como todas as notas de sacrifício devem ser >= 1,
            # o denominador nunca será zero.
            indice_prioridade = beneficio / sacrificio

            ranking.append({
                "id": item.get("id", ""),
                "funcionalidade": nome.strip(),
                "notas": {
                    "valor": valor,
                    "alinhamento_estrategico": alinhamento,
                    "reducao_risco": reducao_risco,
                    "esforco": esforco,
                    "custo": custo,
                },
                "beneficio_ponderado": round(beneficio, 4),
                "sacrificio_ponderado": round(sacrificio, 4),
                "indice_prioridade": round(indice_prioridade, 4),
            })

        # Ordenação:
        # 1. Maior índice de prioridade.
        # 2. Maior benefício ponderado em caso de empate.
        # 3. Menor sacrifício ponderado em caso de novo empate.
        ranking.sort(
            key=lambda item: (
                -item["indice_prioridade"],
                -item["beneficio_ponderado"],
                item["sacrificio_ponderado"],
            )
        )

        # Atribuir posição no ranking após a ordenação.
        for posicao, item in enumerate(ranking, start=1):
            item["prioridade_rank"] = posicao

        return ranking

    # ---------------------------------------------------------
    # EXECUÇÃO INTEGRADA
    # ---------------------------------------------------------

    @staticmethod
    def analisar(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa as análises solicitadas no JSON.

        É permitido informar:
        - somente gva;
        - somente backlog;
        - gva e backlog simultaneamente.
        """
        payload = CalculadoraGVA._validar_objeto(
            payload, "entrada"
        )

        possui_gva = "gva" in payload
        possui_backlog = "backlog" in payload

        if not possui_gva and not possui_backlog:
            raise ValueError(
                "Informe pelo menos uma seção: 'gva' ou 'backlog'."
            )

        saida = {}

        if possui_gva:
            saida["gva_agil"] = CalculadoraGVA.calcular_gva(
                payload["gva"]
            )

        if possui_backlog:
            saida["priorizacao_backlog"] = (
                CalculadoraGVA.priorizar_backlog(
                    payload["backlog"],
                    payload.get("pesos_priorizacao"),
                )
            )

        return saida


# -------------------------------------------------------------
# INTERFACE DE LINHA DE COMANDO (CLI)
# -------------------------------------------------------------

def main() -> None:
    """
    Permite executar o script por arquivo JSON, argumento --json
    ou entrada padrão (stdin).

    Exemplos:

    py calc_gva.py --file dados_gva.json

    py calc_gva.py --json "{\"gva\": {...}}"

    type dados_gva.json | py calc_gva.py
    """

    parser = argparse.ArgumentParser(
        description=(
            "Calculadora de GVA/EVM Ágil e priorização econômica "
            "de backlog."
        )
    )

    grupo_entrada = parser.add_mutually_exclusive_group()

    grupo_entrada.add_argument(
        "--json",
        type=str,
        help="Dados de entrada em formato JSON.",
    )

    grupo_entrada.add_argument(
        "--file",
        type=str,
        help="Caminho para um arquivo JSON.",
    )

    args = parser.parse_args()

    try:
        # Carregar os dados conforme a origem selecionada.
        if args.file:
            with open(args.file, "r", encoding="utf-8") as arquivo:
                payload = json.load(arquivo)

        elif args.json:
            payload = json.loads(args.json)

        else:
            payload = json.load(sys.stdin)

        # Executar as análises solicitadas.
        resultado = CalculadoraGVA.analisar(payload)

        print(
            json.dumps(
                resultado,
                indent=2,
                ensure_ascii=False,
                allow_nan=False,
            )
        )

    except json.JSONDecodeError as exc:
        # JSONDecodeError herda de ValueError.
        # Por isso, deve ser tratado antes de ValueError.
        mensagem = (
            "JSON inválido: {} (linha {}, coluna {}).".format(
                exc.msg,
                exc.lineno,
                exc.colno,
            )
        )
        print(
            json.dumps({"erro": mensagem}, ensure_ascii=False),
            file=sys.stderr,
        )
        sys.exit(1)

    except (ValueError, TypeError, KeyError, OverflowError) as exc:
        # Erros esperados de validação ou processamento.
        print(
            json.dumps({"erro": str(exc)}, ensure_ascii=False),
            file=sys.stderr,
        )
        sys.exit(1)

    except OSError as exc:
        # Problemas de acesso ao arquivo informado.
        mensagem = "Erro de leitura do arquivo: {}".format(exc)
        print(
            json.dumps({"erro": mensagem}, ensure_ascii=False),
            file=sys.stderr,
        )
        sys.exit(1)

    except Exception as exc:
        # Falhas inesperadas: registrar mensagem sem esconder
        # a ocorrência de um erro de programação.
        mensagem = "Erro interno inesperado: {}".format(exc)
        print(
            json.dumps({"erro": mensagem}, ensure_ascii=False),
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
