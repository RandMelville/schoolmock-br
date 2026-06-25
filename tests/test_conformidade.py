"""Garante o achado antes/depois: v1 não-conforme, v2 100% conforme (C1–C5)."""

from datetime import date

from schoolmock_br.benchmark import DATA_REFERENCIA_PADRAO, rodar_benchmark

REF = date(2026, 6, 15)


def test_v2_e_totalmente_conforme_e_supera_v1():
    v1, v2 = rodar_benchmark(seed=42, n_por_serie=30, n_escolas=100, data_referencia=REF)

    # v1 (ingênuo) é amplamente não-conforme.
    assert v1.alunos.taxa_conformidade < 0.5
    assert v1.escolas.taxa_conformidade < 0.1

    # v2 é 100% conforme em alunos e escolas.
    assert v2.alunos.taxa_conformidade == 1.0, v2.alunos.violacoes_por_criterio
    assert v2.escolas.taxa_conformidade == 1.0, v2.escolas.violacoes_por_criterio


def test_benchmark_numeros_publicados_sao_reprodutiveis():
    """Trava os números exatos citados no paper (JOSS/arXiv): defaults do CLI
    (seed 42, 50 alunos/série × 12 séries = 600; 200 escolas) com a data de
    referência fixa do benchmark. Se algum mudar, o paper precisa ser atualizado."""
    # data de referência padrão (a mesma usada por `schoolmock benchmark --seed 42`)
    assert DATA_REFERENCIA_PADRAO == date(2026, 6, 15)

    v1, v2 = rodar_benchmark(seed=42)  # defaults: n_por_serie=50, n_escolas=200

    assert (v1.alunos.total, v1.alunos.conformes) == (600, 195)   # 32,5% — falha C3
    assert (v1.escolas.total, v1.escolas.conformes) == (200, 4)   # 2,0%  — falha C2
    assert v2.alunos.conformes == v2.alunos.total == 600          # 100%
    assert v2.escolas.conformes == v2.escolas.total == 200        # 100%
