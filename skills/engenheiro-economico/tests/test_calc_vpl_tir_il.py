import unittest

from scripts.calc_vpl_tir import CalculadoraEngenhariaEconomica as Calculadora


def analisar(payload):
    return Calculadora.analisar_projeto(payload)


def il(payload):
    return analisar(payload)["indicadores_viabilidade"]["indice_lucratividade"]


class TestIndiceLucratividadeBeneficioCusto(unittest.TestCase):
    def test_beneficios_e_custos_simultaneos_no_mesmo_periodo(self):
        payload = {
            "tma": 0,
            "capex_inicial": 100,
            "periodos": [{"receita_bruta": 100, "opex": 100, "capex_adicional": 50}],
        }
        self.assertEqual(il(payload), 0.4)  # 100 / (100 + 100 + 50)

    def test_capex_inicial_e_capital_de_giro_inicial(self):
        payload = {
            "tma": 0.1,
            "capex_inicial": 100,
            "capital_giro": 20,
            "periodos": [{"receita_bruta": 132}],
        }
        # FC final inclui a recuperação dos R$ 20 de capital de giro:
        # VP(benefícios) = (132 + 20) / 1,1; VP(custos) = 120.
        self.assertAlmostEqual(il(payload), (152 / 1.1) / 120, places=4)

    def test_capex_adicional_e_opex_sao_custos(self):
        payload = {
            "tma": 0,
            "capex_inicial": 50,
            "periodos": [{"receita_bruta": 200, "opex": 30, "capex_adicional": 20}],
        }
        self.assertEqual(il(payload), 2.0)  # 200 / (50 + 30 + 20)

    def test_valor_residual_e_recuperacao_de_capital_de_giro(self):
        payload = {
            "tma": 0.1,
            "capex_inicial": 50,
            "capital_giro": 10,
            "valor_residual": 20,
            "periodos": [{"receita_bruta": 100}],
        }
        self.assertAlmostEqual(il(payload), (130 / 1.1) / 60, places=4)

    def test_tributacao_simplificada_reduz_beneficio_uma_vez(self):
        payload = {
            "tma": 0,
            "capex_inicial": 90,
            "aliquota_imposto": 0.1,
            "periodos": [{"receita_bruta": 100}],
        }
        self.assertEqual(il(payload), 1.0)  # benefício líquido = 90

    def test_desconto_respeita_periodo_de_cada_componente(self):
        payload = {
            "tma": 0.1,
            "capex_inicial": 100,
            "periodos": [{}, {"receita_bruta": 121}],
        }
        self.assertAlmostEqual(il(payload), 1.0)

    def test_ausencia_de_custos_retorna_indefinido(self):
        payload = {"tma": 0.1, "periodos": [{"receita_bruta": 100}]}
        self.assertIsNone(il(payload))

    def test_ausencia_de_beneficios_com_custos_retorna_zero(self):
        payload = {"tma": 0.1, "capex_inicial": 100, "periodos": [{}]}
        self.assertEqual(il(payload), 0.0)

    def test_opex_nao_e_deduzido_dos_beneficios_e_somado_ao_custo(self):
        payload = {
            "tma": 0,
            "capex_inicial": 100,
            "periodos": [{"receita_bruta": 200, "opex": 100}],
        }
        self.assertEqual(il(payload), 1.0)

    def test_beneficios_menos_custos_reconstroem_fluxo_liquido(self):
        payload = {
            "tma": 0.12,
            "aliquota_imposto": 0.06,
            "capex_inicial": 55_000,
            "capital_giro": 5_000,
            "valor_residual": 3_000,
            "periodos": [
                {"receita_bruta": 30_000, "opex": 12_000},
                {"receita_bruta": 40_000, "opex": 15_000, "capex_adicional": 2_000},
                {"receita_bruta": 50_000, "opex": 18_000},
            ],
        }
        resultado = analisar(payload)
        fluxos = resultado["fluxo_de_caixa"]

        for indice, linha in enumerate(fluxos):
            if indice == 0:
                beneficios = 0
                custos = payload["capex_inicial"] + payload["capital_giro"]
            else:
                beneficios = (
                    linha["receita_bruta"]
                    - linha["impostos"]
                    + linha["valor_residual"]
                    + linha["recuperacao_capital_giro"]
                )
                custos = linha["opex"] + linha["capex_adicional"]
            self.assertAlmostEqual(beneficios - custos, linha["fluxo_liquido"])

    def test_regressao_dos_demais_indicadores_oficinapro(self):
        payload = {
            "tma": 0.12,
            "aliquota_imposto": 0.06,
            "capex_inicial": 55_000,
            "capital_giro": 5_000,
            "valor_residual": 3_000,
            "periodos": [
                {"receita_bruta": 30_000, "opex": 12_000},
                {"receita_bruta": 40_000, "opex": 15_000, "capex_adicional": 2_000},
                {"receita_bruta": 50_000, "opex": 18_000},
            ],
        }
        indicadores = analisar(payload)["indicadores_viabilidade"]
        self.assertEqual(indicadores["vpl"], -2777.65)
        self.assertEqual(indicadores["tir_periodo_pct"], 9.6283)
        self.assertEqual(indicadores["payback_simples_periodos"], 2.63)
        self.assertIsNone(indicadores["payback_descontado_periodos"])


if __name__ == "__main__":
    unittest.main()
