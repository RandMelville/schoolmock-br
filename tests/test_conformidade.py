"""Garante o achado antes/depois: v1 não-conforme, v2 100% conforme (C1–C5)."""

from datetime import date

from schoolmock_br.benchmark import rodar_benchmark

REF = date(2026, 6, 15)


def test_v2_e_totalmente_conforme_e_supera_v1():
    v1, v2 = rodar_benchmark(seed=42, n_por_serie=30, n_escolas=100, data_referencia=REF)

    # v1 (ingênuo) é amplamente não-conforme.
    assert v1.alunos.taxa_conformidade < 0.5
    assert v1.escolas.taxa_conformidade < 0.1

    # v2 é 100% conforme em alunos e escolas.
    assert v2.alunos.taxa_conformidade == 1.0, v2.alunos.violacoes_por_criterio
    assert v2.escolas.taxa_conformidade == 1.0, v2.escolas.violacoes_por_criterio
