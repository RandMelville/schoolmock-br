"""Tabelas de referência de domínio (IBGE/UF e série→idade)."""

from .ibge import UF_PARA_CODIGO_IBGE, codigo_ibge_da_uf, uf_do_codigo_inep
from .series import faixa_etaria_esperada, normalizar_serie

__all__ = [
    "UF_PARA_CODIGO_IBGE",
    "codigo_ibge_da_uf",
    "uf_do_codigo_inep",
    "faixa_etaria_esperada",
    "normalizar_serie",
]
