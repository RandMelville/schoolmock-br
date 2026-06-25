"""
Benchmark antes/depois: roda o verificador sobre o gerador ingênuo (v1) e sobre o
v2, sobre o mesmo conjunto de séries e a mesma semente. Produz a evidência central
do paper: taxa de não-conformidade do v1 vs v2.

A amostra de séries cobre todo o Ensino Fundamental e Médio justamente para expor a
lacuna G1 do v1 (que só tratava séries contendo "8" ou "9").
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .baseline import SchoolMockBRv1
from .core import Gerador
from .verifier import LoteReport, Verificador

SERIES_AMOSTRA = [
    "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano",
    "6º Ano", "7º Ano", "8º Ano", "9º Ano",
    "1ª Série EM", "2ª Série EM", "3ª Série EM",
]

# Data de referência fixa do benchmark: torna o critério C3 (idade↔série), que é
# calculado contra uma data, determinístico e reprodutível em qualquer dia. Sem
# isto, `schoolmock benchmark` cairia em date.today() e a taxa do v1 variaria.
DATA_REFERENCIA_PADRAO = date(2026, 6, 15)


@dataclass
class ResultadoBenchmark:
    rotulo: str
    alunos: LoteReport
    escolas: LoteReport


def _gerar_alunos_variados(gerar_aluno, n_por_serie: int) -> list[dict]:
    alunos: list[dict] = []
    for serie in SERIES_AMOSTRA:
        for _ in range(n_por_serie):
            alunos.append(gerar_aluno(serie))
    return alunos


def rodar_benchmark(
    *, seed: int = 42, n_por_serie: int = 50, n_escolas: int = 200,
    data_referencia: date | None = None,
) -> list[ResultadoBenchmark]:
    verificador = Verificador(data_referencia=data_referencia or DATA_REFERENCIA_PADRAO)

    v1 = SchoolMockBRv1(seed=seed)
    alunos_v1 = _gerar_alunos_variados(v1.gerar_aluno, n_por_serie)
    escolas_v1 = [v1.gerar_escola() for _ in range(n_escolas)]

    v2 = Gerador(seed=seed)
    alunos_v2 = _gerar_alunos_variados(v2.gerar_aluno, n_por_serie)
    escolas_v2 = [v2.gerar_escola() for _ in range(n_escolas)]

    return [
        ResultadoBenchmark(
            "v1 (ingênuo / baseline)",
            verificador.verificar_lote_alunos(alunos_v1),
            verificador.verificar_lote_escolas(escolas_v1),
        ),
        ResultadoBenchmark(
            "v2 (atual)",
            verificador.verificar_lote_alunos(alunos_v2),
            verificador.verificar_lote_escolas(escolas_v2),
        ),
    ]


def formatar_relatorio(resultados: list[ResultadoBenchmark]) -> str:
    blocos = ["=" * 64, "BENCHMARK SchoolMock-BR — conformidade (verificador C1–C5)", "=" * 64]
    for r in resultados:
        blocos.append(f"\n### {r.rotulo}")
        blocos.append(r.alunos.resumo())
        blocos.append("")
        blocos.append(r.escolas.resumo())
    return "\n".join(blocos)
