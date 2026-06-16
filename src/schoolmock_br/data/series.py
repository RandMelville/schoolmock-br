"""
Tabela canônica série escolar → faixa etária esperada (idade adequada).

Base do critério C3 do verificador (idade↔série) e da futura correção F1.
A "idade adequada" segue a organização da Educação Básica brasileira, considerando
a idade da criança/jovem no início do ano letivo:

    Educação Infantil  - Creche:      0 a 3 anos
                         Pré-escola:   4 a 5 anos
    Ensino Fundamental - 1º ao 9º ano: 6 a 14 anos (idade = 5 + n)
    Ensino Médio       - 1ª a 3ª série: 15 a 17 anos (idade = 14 + n)

O parsing é tolerante a variações de escrita ("8º Ano", "8o ano", "oitavo ano",
"1ª série EM", "1 ano do ensino médio", etc.).
"""

from __future__ import annotations

import re
import unicodedata

# Faixas fixas (idade_min, idade_max) por estágio não-numerado.
FAIXA_CRECHE = (0, 3)
FAIXA_PRE_ESCOLA = (4, 5)

_ORDINAIS_EXTENSO = {
    "primeiro": 1, "primeira": 1, "segundo": 2, "segunda": 2,
    "terceiro": 3, "terceira": 3, "quarto": 4, "quarta": 4,
    "quinto": 5, "quinta": 5, "sexto": 6, "sexta": 6,
    "setimo": 7, "setima": 7, "oitavo": 8, "oitava": 8,
    "nono": 9, "nona": 9,
}


def _sem_acento(texto: str) -> str:
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch)).lower().strip()


def normalizar_serie(serie: str) -> str:
    """Normaliza a string da série (minúsculas, sem acento, espaços colapsados)."""
    if not isinstance(serie, str):
        return ""
    return re.sub(r"\s+", " ", _sem_acento(serie))


def _extrair_ordinal(texto: str) -> int | None:
    """Extrai o número da série (1-9), seja em dígito ou por extenso."""
    m = re.search(r"\d{1,2}", texto)
    if m:
        n = int(m.group(0))
        if 1 <= n <= 9:
            return n
    for palavra, valor in _ORDINAIS_EXTENSO.items():
        if palavra in texto:
            return valor
    return None


def faixa_etaria_esperada(serie: str) -> tuple[int, int] | None:
    """
    Retorna (idade_min, idade_max) esperada para a série, ou None se não reconhecida.

    A faixa é a idade adequada ± a granularidade natural do estágio; o verificador
    aplica ainda uma tolerância adicional configurável.
    """
    t = normalizar_serie(serie)
    if not t:
        return None

    # Educação Infantil
    if "creche" in t:
        return FAIXA_CRECHE
    if "pre" in t and ("escola" in t or "infantil" in t):
        return FAIXA_PRE_ESCOLA
    if "infantil" in t and _extrair_ordinal(t) is None:
        return (0, 5)

    n = _extrair_ordinal(t)
    if n is None:
        return None

    eh_medio = ("medio" in t) or bool(re.search(r"\bem\b", t)) or ("ensino medio" in t)
    if eh_medio:
        if not 1 <= n <= 3:
            return None
        idade = 14 + n  # 1ª série EM -> 15
        return (idade, idade)

    # Padrão: Ensino Fundamental (1º ao 9º ano)
    idade = 5 + n  # 1º ano EF -> 6
    return (idade, idade)
