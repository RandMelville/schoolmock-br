"""
Construtor de dataset educacional sintético com vínculo escola↔turma↔aluno.

Gera uma estrutura relacional (escolas, turmas, alunos) com:
  * reprodutibilidade total via `seed` (F4);
  * identificadores únicos em todo o lote — codigo_inep, cpf, matricula (critério C5);
  * coerência por construção — idade↔série (C3) e INEP↔UF (C2), herdadas do `Gerador`;
  * marcação explícita de origem sintética em cada registro (`fonte`), para o datasheet;
  * export JSON (arquivo único relacional) ou CSV (uma tabela por entidade).

É a base do dataset citável (DOI/CC-BY) descrito no PLANO-V2.
"""

from __future__ import annotations

import csv
import json
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from . import __version__
from .core import Gerador
from .data.series import normalizar_serie
from .verifier import Verificador

FONTE = f"SchoolMock-BR v{__version__} (dados sintéticos)"

SERIES_PADRAO: tuple[str, ...] = (
    "1º Ano", "2º Ano", "3º Ano", "4º Ano", "5º Ano",
    "6º Ano", "7º Ano", "8º Ano", "9º Ano",
    "1ª Série EM", "2ª Série EM", "3ª Série EM",
)

_TURNOS = ("Matutino", "Vespertino")
_TURNOS_EM = ("Matutino", "Vespertino", "Noturno")


@dataclass
class Dataset:
    """Dataset relacional sintético + metadados."""

    escolas: list[dict]
    turmas: list[dict]
    alunos: list[dict]
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "metadata": self.metadata,
            "escolas": self.escolas,
            "turmas": self.turmas,
            "alunos": self.alunos,
        }

    def export_json(self, caminho: str | Path) -> Path:
        caminho = Path(caminho)
        conteudo = json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
        caminho.write_text(conteudo, encoding="utf-8")
        return caminho

    def export_csv(self, diretorio: str | Path) -> list[Path]:
        diretorio = Path(diretorio)
        diretorio.mkdir(parents=True, exist_ok=True)
        escritos: list[Path] = []
        for nome, registros in (
            ("escolas", self.escolas),
            ("turmas", self.turmas),
            ("alunos", self.alunos),
        ):
            caminho = diretorio / f"{nome}.csv"
            _escrever_csv(caminho, registros)
            escritos.append(caminho)
        meta = diretorio / "metadata.json"
        meta.write_text(json.dumps(self.metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        escritos.append(meta)
        return escritos


def _escrever_csv(caminho: Path, registros: list[dict]) -> None:
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        if not registros:
            return
        writer = csv.DictWriter(fh, fieldnames=list(registros[0].keys()))
        writer.writeheader()
        writer.writerows(registros)


def _gerar_unico(
    gerar: Callable[[], dict], chaves: tuple[str, ...], vistos: dict[str, set]
) -> dict:
    """Gera um registro até que todos os valores em `chaves` sejam inéditos no lote."""
    while True:
        rec = gerar()
        if all(rec[c] not in vistos[c] for c in chaves):
            for c in chaves:
                vistos[c].add(rec[c])
            return rec


def _turnos_da_serie(serie: str):
    norm = normalizar_serie(serie)
    return _TURNOS_EM if ("em" in norm or "medio" in norm) else _TURNOS


def construir_dataset(
    *,
    seed: int = 42,
    n_escolas: int = 10,
    turmas_por_escola: tuple[int, int] = (2, 5),
    alunos_por_turma: tuple[int, int] = (20, 35),
    series: tuple[str, ...] = SERIES_PADRAO,
    ano_letivo: int = 2026,
    verificar: bool = True,
) -> Dataset:
    """
    Constrói um dataset relacional sintético reprodutível.

    Args:
        seed: semente para reprodutibilidade total.
        n_escolas: número de escolas.
        turmas_por_escola: faixa (min, max) de turmas por escola.
        alunos_por_turma: faixa (min, max) de alunos por turma.
        series: séries elegíveis para as turmas.
        ano_letivo: ano letivo registrado em turmas/metadados.
        verificar: se True, roda o verificador e anexa o resumo de conformidade aos metadados.
    """
    gerador = Gerador(seed=seed)
    rng = gerador._rng  # mesma fonte semeada, para amostragem reprodutível das contagens

    vistos_escola = {"codigo_inep": set()}
    vistos_aluno = {"cpf": set(), "matricula": set()}

    escolas: list[dict] = []
    turmas: list[dict] = []
    alunos: list[dict] = []

    for _ in range(n_escolas):
        escola = _gerar_unico(gerador.gerar_escola, ("codigo_inep",), vistos_escola)
        escola = {**escola, "fonte": FONTE}
        escolas.append(escola)

        n_turmas = rng.randint(*turmas_por_escola)
        for t in range(n_turmas):
            serie = rng.choice(series)
            turno = rng.choice(_turnos_da_serie(serie))
            turma_id = f"{escola['codigo_inep']}-{t + 1:02d}"
            n_alunos = rng.randint(*alunos_por_turma)

            for _ in range(n_alunos):
                aluno = _gerar_unico(
                    lambda: gerador.gerar_aluno(serie),  # noqa: B023 (serie é estável no escopo da turma)
                    ("cpf", "matricula"),
                    vistos_aluno,
                )
                aluno = {
                    "turma_id": turma_id,
                    "codigo_inep": escola["codigo_inep"],
                    **aluno,
                    "fonte": FONTE,
                }
                alunos.append(aluno)

            turmas.append({
                "turma_id": turma_id,
                "codigo_inep": escola["codigo_inep"],
                "serie": serie,
                "turno": turno,
                "ano_letivo": ano_letivo,
                "qtd_alunos": n_alunos,
                "fonte": FONTE,
            })

    metadata = {
        "gerador": "SchoolMock-BR",
        "versao": __version__,
        "tipo": "dados educacionais sintéticos (procedural, LGPD-safe)",
        "seed": seed,
        "ano_letivo": ano_letivo,
        "gerado_em": date.today().isoformat(),
        "contagens": {"escolas": len(escolas), "turmas": len(turmas), "alunos": len(alunos)},
        "aviso": (
            "Todos os registros são FICTÍCIOS, gerados proceduralmente. "
            "Não correspondem a pessoas reais."
        ),
    }

    dataset = Dataset(escolas=escolas, turmas=turmas, alunos=alunos, metadata=metadata)

    if verificar:
        verif = Verificador()
        rep_alunos = verif.verificar_lote_alunos(alunos)
        rep_escolas = verif.verificar_lote_escolas(escolas)
        metadata["conformidade"] = {
            "alunos": {
                "taxa": round(rep_alunos.taxa_conformidade, 4),
                "violacoes_por_criterio": rep_alunos.violacoes_por_criterio,
            },
            "escolas": {
                "taxa": round(rep_escolas.taxa_conformidade, 4),
                "violacoes_por_criterio": rep_escolas.violacoes_por_criterio,
            },
        }

    return dataset
