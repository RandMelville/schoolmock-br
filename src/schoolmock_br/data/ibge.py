"""
Códigos IBGE das Unidades da Federação.

No padrão do Censo Escolar/INEP, os 2 primeiros dígitos do código INEP da escola
(8 dígitos) correspondem ao código IBGE da UF. Esta tabela é a fonte de verdade
usada pelo critério C2 do verificador (INEP↔UF) e, futuramente, pela correção F2.
"""

from __future__ import annotations

# UF -> código IBGE (2 dígitos). Fonte: tabela de UFs do IBGE.
UF_PARA_CODIGO_IBGE: dict[str, int] = {
    "RO": 11, "AC": 12, "AM": 13, "RR": 14, "PA": 15, "AP": 16, "TO": 17,
    "MA": 21, "PI": 22, "CE": 23, "RN": 24, "PB": 25, "PE": 26, "AL": 27,
    "SE": 28, "BA": 29,
    "MG": 31, "ES": 32, "RJ": 33, "SP": 35,
    "PR": 41, "SC": 42, "RS": 43,
    "MS": 50, "MT": 51, "GO": 52, "DF": 53,
}

# Mapa inverso: código IBGE (2 dígitos) -> UF.
CODIGO_IBGE_PARA_UF: dict[int, str] = {v: k for k, v in UF_PARA_CODIGO_IBGE.items()}

UFS: tuple[str, ...] = tuple(UF_PARA_CODIGO_IBGE.keys())


def codigo_ibge_da_uf(uf: str) -> int | None:
    """Retorna o código IBGE (2 dígitos) de uma UF, ou None se desconhecida."""
    if not isinstance(uf, str):
        return None
    return UF_PARA_CODIGO_IBGE.get(uf.strip().upper())


def uf_do_codigo_inep(codigo_inep: str | int) -> str | None:
    """
    Deriva a UF a partir dos 2 primeiros dígitos de um código INEP.

    Retorna None se o código não tiver pelo menos 2 dígitos ou o prefixo não
    corresponder a nenhuma UF válida.
    """
    digitos = "".join(ch for ch in str(codigo_inep) if ch.isdigit())
    if len(digitos) < 2:
        return None
    prefixo = int(digitos[:2])
    return CODIGO_IBGE_PARA_UF.get(prefixo)
