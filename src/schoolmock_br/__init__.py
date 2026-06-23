"""
SchoolMock-BR v2 — gerador procedural de dados educacionais brasileiros sintéticos
(LGPD-safe) com camada de verificação determinística.

API estável (retrocompatível com o v1, ISBN 978-65-01-89921-3):
    SchoolMockBR.gerar_aluno / gerar_escola / gerar_turma_lote

Novidades do v2:
    Gerador(seed=...)        gerador reprodutível (F4)
    Verificador              camada verificadora C1–C5 (F5)
    modo_teste / cpf_marcado_para_teste   CPFs reconhecíveis como sintéticos (F3)
"""

from __future__ import annotations

from .core import Gerador, SchoolMockBR
from .cpf import cpf_marcado_para_teste, cpf_valido
from .verifier import LoteReport, RegistroReport, Verificador, Violacao

__version__ = "2.1.0"

__all__ = [
    "SchoolMockBR",
    "Gerador",
    "Verificador",
    "LoteReport",
    "RegistroReport",
    "Violacao",
    "cpf_valido",
    "cpf_marcado_para_teste",
    "__version__",
]
