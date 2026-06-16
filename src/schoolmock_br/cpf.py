"""
Utilitários de CPF: geração (mod-11), validação e marcação para teste (F3).

O critério C1 do verificador exige CPF (a) válido pelo dígito verificador (mod-11)
e (b) não pertencente ao conjunto de sequências conhecidas-inválidas (todos os
dígitos iguais), que passam no mod-11 mas são rejeitadas por sistemas reais.

Risco residual de colisão (F3)
------------------------------
Existem ~10^9 CPFs válidos por mod-11 (9 dígitos-base livres; os 2 verificadores
são determinados). A base instalada de CPFs já atribuídos pela Receita Federal é
da ordem de ~2×10^8. Logo, *qualquer* gerador de CPFs válidos uniformes tem chance
não-desprezível de produzir um número que coincide com o de uma pessoa real — e
**não existe faixa oficial de "CPF de teste" reservada pela Receita** que elimine
isso. O `modo_teste` (abaixo) NÃO garante não-colisão; ele torna o CPF
*reconhecível como sintético* via um prefixo sentinela documentado
(`PREFIXO_TESTE`), permitindo que qualquer consumidor detecte e filtre os
registros (`cpf_marcado_para_teste`). É defesa em profundidade, complementar à
marcação de origem já presente no registro (`fonte`) e nos metadados do dataset.
"""

from __future__ import annotations

import random

# CPFs de dígitos repetidos passam no mod-11 mas são universalmente inválidos.
SEQUENCIAS_INVALIDAS: frozenset[str] = frozenset(str(d) * 11 for d in range(10))

# Prefixo sentinela do modo_teste: os primeiros dígitos do CPF ficam fixos neste
# valor, tornando o número reconhecível como sintético. Mantém-se a validade
# mod-11 (C1 continua passando) e restam 10^(11-2-len(PREFIXO_TESTE)) bases livres
# — com PREFIXO_TESTE="999", ~10^6 CPFs únicos, folga ampla para datasets de pesquisa.
PREFIXO_TESTE: str = "999"


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


def cpf_marcado_para_teste(cpf: str | int) -> bool:
    """
    True se o CPF é válido E começa com `PREFIXO_TESTE`, isto é, foi gerado em
    `modo_teste` e é reconhecível como sintético. Permite filtrar/auditar lotes.
    """
    d = apenas_digitos(cpf)
    return cpf_valido(d) and d.startswith(PREFIXO_TESTE)


def gerar_cpf(
    rng: random.Random, *, rejeitar_invalidos: bool = True, modo_teste: bool = False
) -> str:
    """
    Gera um CPF formatado, válido por mod-11.

    Quando rejeitar_invalidos=True (padrão do v2), reamostra caso caia numa
    sequência conhecida-inválida. O caminho ingênuo do v1 não fazia essa rejeição.

    Quando modo_teste=True (F3), fixa os primeiros dígitos em `PREFIXO_TESTE`,
    produzindo um CPF válido porém reconhecível como sintético
    (ver `cpf_marcado_para_teste` e a nota de risco residual no topo do módulo).
    """
    n_prefixo = len(PREFIXO_TESTE) if modo_teste else 0
    fixos = [int(c) for c in PREFIXO_TESTE] if modo_teste else []
    while True:
        base = fixos + [rng.randint(0, 9) for _ in range(9 - n_prefixo)]
        dv1 = _digito_verificador(base)
        dv2 = _digito_verificador(base + [dv1])
        digitos = "".join(str(x) for x in base + [dv1, dv2])
        if not rejeitar_invalidos or digitos not in SEQUENCIAS_INVALIDAS:
            return formatar_cpf(digitos)
