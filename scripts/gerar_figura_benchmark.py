"""
Gera a figura do benchmark de conformidade (v1 ingênuo vs v2 verificado) usada
no paper JOSS, a partir dos números REAIS do `rodar_benchmark` — assim a figura
nunca diverge do que o software produz.

Uso:
    python scripts/gerar_figura_benchmark.py
Saída: paper/benchmark.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from schoolmock_br.benchmark import rodar_benchmark  # noqa: E402

SAIDA = Path(__file__).resolve().parent.parent / "paper" / "benchmark.png"


def main() -> None:
    v1, v2 = rodar_benchmark(seed=42)  # data de referência fixa do benchmark

    grupos = ["Students", "Schools"]
    taxas_v1 = [v1.alunos.taxa_conformidade * 100, v1.escolas.taxa_conformidade * 100]
    taxas_v2 = [v2.alunos.taxa_conformidade * 100, v2.escolas.taxa_conformidade * 100]

    x = range(len(grupos))
    largura = 0.36

    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    b1 = ax.bar([i - largura / 2 for i in x], taxas_v1, largura,
                label="v1 (naive, no verifier)", color="#c0392b")
    b2 = ax.bar([i + largura / 2 for i in x], taxas_v2, largura,
                label="v2 (with verifier)", color="#27ae60")

    ax.set_ylabel("Structurally conformant records (%)")
    ax.set_ylim(0, 105)
    ax.set_xticks(list(x))
    ax.set_xticklabels(grupos)
    ax.legend(frameon=False, loc="center right")
    ax.spines[["top", "right"]].set_visible(False)

    for barras in (b1, b2):
        for b in barras:
            ax.annotate(f"{b.get_height():.1f}%",
                        (b.get_x() + b.get_width() / 2, b.get_height()),
                        textcoords="offset points", xytext=(0, 3),
                        ha="center", fontsize=9)

    fig.tight_layout()
    fig.savefig(SAIDA, dpi=200)
    print(f"Figura salva em {SAIDA}")


if __name__ == "__main__":
    main()
