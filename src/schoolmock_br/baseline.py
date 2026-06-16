"""
Linha de base ingênua (v1) — CONTROLE CIENTÍFICO. NÃO CORRIGIR.

Réplica fiel da lógica de `schoolmock_br.py` (v1 registrado: ISBN 978-65-01-89921-3,
DOI 10.5281/zenodo.18343467), com a ÚNICA adição de semente (seed) para tornar a
medição reprodutível. Todos os defeitos conhecidos (G1–G7 do PLANO-V2) são
preservados intencionalmente: este módulo é o "antes" comparado ao `core.py` (v2).

Rodar o verificador (`schoolmock_br.verifier`) sobre a saída desta classe produz a
taxa de não-conformidade que serve de baseline para o artigo.
"""

from __future__ import annotations

import random

from faker import Faker

_ESTADOS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
    "SP", "SE", "TO",
]


class SchoolMockBRv1:
    """Gerador ingênuo equivalente ao v1, com semente para reprodutibilidade."""

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)
        self._fake = Faker("pt_BR")
        if seed is not None:
            self._fake.seed_instance(seed)

    def _gerar_cpf_valido(self) -> str:
        # G3: válido por mod-11, mas NÃO rejeita sequências conhecidas-inválidas.
        cpf = [self._rng.randint(0, 9) for _ in range(9)]
        for _ in range(2):
            val = sum((len(cpf) + 1 - i) * v for i, v in enumerate(cpf)) % 11
            cpf.append(11 - val if val > 1 else 0)
        return "%s%s%s.%s%s%s.%s%s%s-%s%s" % tuple(cpf)  # noqa: UP031 (cópia fiel do v1)

    def gerar_aluno(self, serie_escolar: str = "8º Ano") -> dict:
        # G1: só "8" e "9" são tratados; qualquer outra série cai em idade_base=6.
        idade_base = 6
        if "8" in serie_escolar:
            idade_base = 13
        elif "9" in serie_escolar:
            idade_base = 14

        nascimento = self._fake.date_of_birth(
            minimum_age=idade_base - 1, maximum_age=idade_base + 1
        )
        return {
            "nome_completo": self._fake.name(),
            "cpf": self._gerar_cpf_valido(),
            "data_nascimento": nascimento.strftime("%d/%m/%Y"),
            "nome_mae": self._fake.name_female(),
            "matricula": str(self._rng.randint(10000000, 99999999)),
            "situacao": self._rng.choice(["Cursando", "Cursando", "Cursando", "Transferido"]),
            "serie_atual": serie_escolar,
        }

    def gerar_escola(self) -> dict:
        # G2: UF sorteada à parte; código INEP aleatório, sem vínculo com a UF.
        uf = self._rng.choice(_ESTADOS)
        return {
            "nome_escola": f"Escola Estadual {self._fake.last_name()} {self._fake.city_suffix()}",
            "codigo_inep": str(self._rng.randint(11000000, 53999999)),
            "endereco": self._fake.street_address(),
            "cidade": self._fake.city(),
            "uf": uf,
            "rede": "Pública Estadual",
        }

    def gerar_turma_lote(self, qtd: int = 10, serie: str = "8º Ano") -> list[dict]:
        return [self.gerar_aluno(serie) for _ in range(qtd)]
