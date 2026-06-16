"""
Camada verificadora determinística (F5) — peça central do v2 e instrumento do paper.

Critérios:
    C1  CPF válido (mod-11) e não pertencente a sequências conhecidas-inválidas.
    C2  Código INEP consistente com a UF (2 primeiros dígitos = código IBGE da UF).
    C3  Idade coerente com a série (data_nascimento ↔ serie_atual).
    C4  Campos obrigatórios presentes e não vazios.
    C5  Unicidade de identificadores no lote (cpf, matricula, codigo_inep).

A verificação é determinística: dada a mesma entrada e a mesma `data_referencia`,
o veredito é sempre o mesmo. Rodar sobre `baseline.SchoolMockBRv1` (v1) vs `core`
(v2) produz o achado empírico antes/depois.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from .cpf import cpf_valido
from .data.ibge import uf_do_codigo_inep
from .data.series import faixa_etaria_esperada

CAMPOS_OBRIGATORIOS_ALUNO = ("nome_completo", "cpf", "data_nascimento", "serie_atual", "matricula")
CAMPOS_OBRIGATORIOS_ESCOLA = ("nome_escola", "codigo_inep", "uf")


@dataclass(frozen=True)
class Violacao:
    """Uma falha de critério em um registro."""

    criterio: str  # "C1".."C5"
    nome: str
    detalhe: str


@dataclass
class RegistroReport:
    """Resultado da verificação de um único registro."""

    indice: int
    tipo: str  # "aluno" | "escola"
    violacoes: list[Violacao] = field(default_factory=list)

    @property
    def conforme(self) -> bool:
        return not self.violacoes


@dataclass
class LoteReport:
    """Relatório agregado de um lote de registros."""

    tipo: str
    total: int
    registros: list[RegistroReport]
    violacoes_por_criterio: dict[str, int]

    @property
    def conformes(self) -> int:
        return sum(1 for r in self.registros if r.conforme)

    @property
    def nao_conformes(self) -> int:
        return self.total - self.conformes

    @property
    def taxa_conformidade(self) -> float:
        return self.conformes / self.total if self.total else 1.0

    def resumo(self) -> str:
        linhas = [
            f"Lote de {self.tipo}: {self.total} registros",
            f"  conformes:     {self.conformes} ({self.taxa_conformidade:.1%})",
            f"  não-conformes: {self.nao_conformes}",
            "  violações por critério:",
        ]
        for crit in sorted(self.violacoes_por_criterio):
            linhas.append(f"    {crit}: {self.violacoes_por_criterio[crit]}")
        return "\n".join(linhas)


def _idade_em(nascimento: date, referencia: date) -> int:
    anos = referencia.year - nascimento.year
    if (referencia.month, referencia.day) < (nascimento.month, nascimento.day):
        anos -= 1
    return anos


def _parse_data(valor: str) -> date | None:
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            from datetime import datetime

            return datetime.strptime(valor, fmt).date()
        except (ValueError, TypeError):
            continue
    return None


class Verificador:
    """Aplica os critérios C1–C5. Veja o módulo para a definição de cada critério."""

    def __init__(self, *, tolerancia_idade: int = 1, data_referencia: date | None = None) -> None:
        self.tolerancia_idade = tolerancia_idade
        self.data_referencia = data_referencia or date.today()

    # ---- critérios por registro -------------------------------------------------

    def _c1_cpf(self, aluno: dict) -> Violacao | None:
        cpf = aluno.get("cpf", "")
        if not cpf_valido(cpf):
            return Violacao("C1", "CPF válido", f"CPF inválido ou conhecido-inválido: {cpf!r}")
        return None

    def _c3_idade_serie(self, aluno: dict) -> Violacao | None:
        serie = aluno.get("serie_atual", "")
        faixa = faixa_etaria_esperada(serie)
        if faixa is None:
            return Violacao("C3", "Idade↔série", f"série não reconhecida: {serie!r}")
        bruto = aluno.get("data_nascimento", "")
        nascimento = _parse_data(bruto)
        if nascimento is None:
            return Violacao("C3", "Idade↔série", f"data inválida: {bruto!r}")
        idade = _idade_em(nascimento, self.data_referencia)
        minimo, maximo = faixa
        if not (minimo - self.tolerancia_idade <= idade <= maximo + self.tolerancia_idade):
            return Violacao(
                "C3", "Idade↔série",
                f"idade {idade} fora da faixa {minimo}-{maximo} (±{self.tolerancia_idade}) "
                f"para {aluno.get('serie_atual')!r}",
            )
        return None

    def _c2_inep_uf(self, escola: dict) -> Violacao | None:
        inep = escola.get("codigo_inep", "")
        uf_declarada = str(escola.get("uf", "")).strip().upper()
        uf_derivada = uf_do_codigo_inep(inep)
        if uf_derivada is None:
            return Violacao("C2", "INEP↔UF", f"prefixo do INEP não mapeia para UF: {inep!r}")
        if uf_derivada != uf_declarada:
            return Violacao(
                "C2", "INEP↔UF",
                f"INEP {inep!r} aponta para {uf_derivada}, mas uf={uf_declarada!r}",
            )
        return None

    def _c4_campos(self, registro: dict, obrigatorios: tuple[str, ...]) -> Violacao | None:
        faltando = [c for c in obrigatorios if not str(registro.get(c, "")).strip()]
        if faltando:
            return Violacao("C4", "Campos obrigatórios", f"ausentes/vazios: {', '.join(faltando)}")
        return None

    # ---- API por registro -------------------------------------------------------

    def verificar_aluno(self, aluno: dict, indice: int = 0) -> RegistroReport:
        rep = RegistroReport(indice=indice, tipo="aluno")
        for v in (
            self._c4_campos(aluno, CAMPOS_OBRIGATORIOS_ALUNO),
            self._c1_cpf(aluno),
            self._c3_idade_serie(aluno),
        ):
            if v is not None:
                rep.violacoes.append(v)
        return rep

    def verificar_escola(self, escola: dict, indice: int = 0) -> RegistroReport:
        rep = RegistroReport(indice=indice, tipo="escola")
        for v in (
            self._c4_campos(escola, CAMPOS_OBRIGATORIOS_ESCOLA),
            self._c2_inep_uf(escola),
        ):
            if v is not None:
                rep.violacoes.append(v)
        return rep

    # ---- API por lote (inclui C5: unicidade) ------------------------------------

    def verificar_lote_alunos(self, alunos: list[dict]) -> LoteReport:
        registros = [self.verificar_aluno(a, i) for i, a in enumerate(alunos)]
        self._aplicar_c5(alunos, registros, chaves=("cpf", "matricula"))
        return self._agregar("aluno", registros)

    def verificar_lote_escolas(self, escolas: list[dict]) -> LoteReport:
        registros = [self.verificar_escola(e, i) for i, e in enumerate(escolas)]
        self._aplicar_c5(escolas, registros, chaves=("codigo_inep",))
        return self._agregar("escola", registros)

    def _aplicar_c5(
        self, dados: list[dict], registros: list[RegistroReport], chaves: tuple[str, ...]
    ) -> None:
        for chave in chaves:
            vistos: dict[str, int] = {}
            for i, d in enumerate(dados):
                valor = str(d.get(chave, ""))
                if valor in vistos:
                    registros[i].violacoes.append(
                        Violacao(
                            "C5", "Unicidade",
                            f"{chave} duplicado (= registro #{vistos[valor]}): {valor!r}",
                        )
                    )
                else:
                    vistos[valor] = i

    @staticmethod
    def _agregar(tipo: str, registros: list[RegistroReport]) -> LoteReport:
        por_criterio: dict[str, int] = {}
        for r in registros:
            for v in r.violacoes:
                por_criterio[v.criterio] = por_criterio.get(v.criterio, 0) + 1
        return LoteReport(
            tipo=tipo,
            total=len(registros),
            registros=registros,
            violacoes_por_criterio=por_criterio,
        )
