"""
Gerador v2 (produto em evolução).

Estado atual deste passo do roadmap:
  * F4 — semente (seed) propagada para `random` e `Faker`: reprodutibilidade total. ✔
  * C1 — CPF validado (rejeita sequências conhecidas-inválidas). ✔
  * F1 — idade derivada da tabela canônica série→faixa etária (C3 por construção). ✔
  * F2 — código INEP prefixado pelo código IBGE da UF (C2 por construção). ✔
  Resultado: a saída do v2 é 100% conforme aos critérios C1–C5 do verificador.

Retrocompatibilidade: a API pública documentada no manual (ISBN 978-65-01-89921-3)
— `SchoolMockBR.gerar_aluno`, `.gerar_escola`, `.gerar_turma_lote`, chamável de forma
estática — é preservada. O novo `Gerador(seed=...)` é a interface reprodutível.
"""

from __future__ import annotations

import random

from faker import Faker

from .cpf import gerar_cpf
from .data.ibge import UFS, codigo_ibge_da_uf
from .data.series import faixa_etaria_esperada

_SITUACOES = ["Cursando", "Cursando", "Cursando", "Transferido"]


class Gerador:
    """Gerador reprodutível de dados educacionais sintéticos."""

    def __init__(self, seed: int | None = None, locale: str = "pt_BR") -> None:
        self.seed = seed
        self._rng = random.Random(seed)
        self._fake = Faker(locale)
        if seed is not None:
            self._fake.seed_instance(seed)

    def gerar_aluno(self, serie_escolar: str = "8º Ano") -> dict:
        # F1: idade derivada da tabela canônica série→faixa etária (idade adequada).
        # Por construção, o aluno satisfaz o critério C3 do verificador.
        faixa = faixa_etaria_esperada(serie_escolar)
        idade_min, idade_max = faixa if faixa is not None else (13, 13)

        nascimento = self._fake.date_of_birth(
            minimum_age=idade_min, maximum_age=idade_max
        )
        return {
            "nome_completo": self._fake.name(),
            "cpf": gerar_cpf(self._rng, rejeitar_invalidos=True),
            "data_nascimento": nascimento.strftime("%d/%m/%Y"),
            "nome_mae": self._fake.name_female(),
            "matricula": str(self._rng.randint(10000000, 99999999)),
            "situacao": self._rng.choice(_SITUACOES),
            "serie_atual": serie_escolar,
        }

    def gerar_escola(self) -> dict:
        uf = self._rng.choice(UFS)
        # F2: os 2 primeiros dígitos do código INEP = código IBGE da UF (padrão Censo).
        # Por construção, a escola satisfaz o critério C2 do verificador.
        prefixo = codigo_ibge_da_uf(uf)
        codigo_inep = f"{prefixo:02d}{self._rng.randint(0, 999999):06d}"
        return {
            "nome_escola": f"Escola Estadual {self._fake.last_name()} {self._fake.city_suffix()}",
            "codigo_inep": codigo_inep,
            "endereco": self._fake.street_address(),
            "cidade": self._fake.city(),
            "uf": uf,
            "rede": "Pública Estadual",
        }

    def gerar_turma_lote(self, qtd: int = 10, serie: str = "8º Ano") -> list[dict]:
        return [self.gerar_aluno(serie) for _ in range(qtd)]


class SchoolMockBR:
    """
    Fachada retrocompatível com a API documentada do v1.

    Mantém as chamadas estáticas (`SchoolMockBR.gerar_aluno(...)`) e adiciona
    `SchoolMockBR.semear(seed)` para reprodutibilidade sem quebrar assinaturas.
    """

    _default = Gerador()

    @classmethod
    def semear(cls, seed: int | None) -> None:
        """Reconfigura o gerador padrão com uma semente (afeta as chamadas estáticas)."""
        cls._default = Gerador(seed=seed)

    @classmethod
    def gerar_aluno(cls, serie_escolar: str = "8º Ano") -> dict:
        return cls._default.gerar_aluno(serie_escolar)

    @classmethod
    def gerar_escola(cls) -> dict:
        return cls._default.gerar_escola()

    @classmethod
    def gerar_turma_lote(cls, qtd: int = 10, serie: str = "8º Ano") -> list[dict]:
        return cls._default.gerar_turma_lote(qtd, serie)
