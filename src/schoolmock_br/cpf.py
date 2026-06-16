"""
Utilitários de CPF: geração (mod-11) e validação.

O critério C1 do verificador exige CPF (a) válido pelo dígito verificador (mod-11)
e (b) não pertencente ao conjunto de sequências conhecidas-inválidas (todos os
dígitos iguais), que passam no mod-11 mas são rejeitadas por sistemas reais.
"""

from __future__ import annotations

import random

# CPFs de dígitos repetidos passam no mod-11 mas são universalmente inválidos.
SEQUENCIAS_INVALIDAS: frozenset[str] = frozenset(str(d) * 11 for d in range(10))


def apenas_digitos(cpf: str | int) -> str:
    return "".join(ch for ch in str(cpf) if ch.isdigit())


def _digito_verificador(parciais: list[int]) -> int:
    val = sum((len(parciais) + 1 - i) * v for i, v in enumerate(parciais)) % 11
    return 11 - val if val > 1 else 0


def formatar_cpf(digitos: str) -> str:
    d = apenas_digitos(digitos)
    return f"{d[0:3]}.{d[3:6]}.{d[6:9]}-{d[9:11]}"


def cpf_valido(cpf: str | int) -> bool:
    """True se o CPF tem 11 dígitos, não é sequência repetida e os DVs conferem."""
    d = apenas_digitos(cpf)
    if len(d) != 11 or d in SEQUENCIAS_INVALIDAS:
        return False
    base = [int(x) for x in d[:9]]
    dv1 = _digito_verificador(base)
    dv2 = _digito_verificador(base + [dv1])
    return d[9] == str(dv1) and d[10] == str(dv2)


def gerar_cpf(rng: random.Random, *, rejeitar_invalidos: bool = True) -> str:
    """
    Gera um CPF formatado, válido por mod-11.

    Quando rejeitar_invalidos=True (padrão do v2), reamostra caso caia numa
    sequência conhecida-inválida. O caminho ingênuo do v1 não fazia essa rejeição.
    """
    while True:
        base = [rng.randint(0, 9) for _ in range(9)]
        dv1 = _digito_verificador(base)
        dv2 = _digito_verificador(base + [dv1])
        digitos = "".join(str(x) for x in base + [dv1, dv2])
        if not rejeitar_invalidos or digitos not in SEQUENCIAS_INVALIDAS:
            return formatar_cpf(digitos)
