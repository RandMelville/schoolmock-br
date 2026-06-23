#!/usr/bin/env python3
"""
Receita do **dataset oficial congelado** do SchoolMock-BR.

Este script é a fonte única de verdade do dataset de referência publicado no
Zenodo (DOI próprio, CC-BY 4.0) e espelhado no Hugging Face. Rodá-lo com a mesma
versão da biblioteca reproduz o artefato byte-a-byte — é o que torna o dataset
verificável (qualquer pessoa confere os checksums).

    python scripts/gerar_dataset_oficial.py            # gera em dist-dataset/
    python scripts/gerar_dataset_oficial.py --out X    # diretório de saída alternativo

Parâmetros são CONGELADOS abaixo (não os mude sem subir a versão do dataset).
O artefato NÃO é versionado no Git — só a receita (este arquivo) é.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

# O schoolmock_br.py da RAIZ (v1 congelado) sombrearia o pacote em src/ quando o
# script roda a partir do repositório; priorizamos src/ explicitamente.
_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "src"))

from schoolmock_br import __version__ as LIB_VERSION  # noqa: E402
from schoolmock_br.dataset import construir_dataset  # noqa: E402

# --- Parâmetros congelados do dataset de referência v1.0.0 -------------------
DATASET_VERSION = "1.0.0"
SEED = 2026
N_ESCOLAS = 100
TURMAS_POR_ESCOLA = (3, 6)
ALUNOS_POR_TURMA = (20, 35)
ANO_LETIVO = 2026
# Data de geração FIXA: mantém os metadados reprodutíveis byte-a-byte
# (o conteúdo já é determinístico pela seed; este campo, não — por isso é fixado).
DATA_GERACAO = "2026-06-23"

LICENCA = "CC-BY-4.0"
TITULO = "SchoolMock-BR — Dataset Educacional Sintético de Referência"
AUTOR = "Randerson Oliveira Melville Rebouças (PPGIE/UFRGS)"
# DOI do dataset no Zenodo (emitido na publicação). Preencher quando reservado;
# enquanto None, o card mostra "(a ser emitido)".
DOI_DATASET: str | None = None
# -----------------------------------------------------------------------------


def _card_md(contagens: dict, conformidade: dict) -> str:
    """Dataset card (README) com front-matter do Hugging Face; serve também ao Zenodo."""
    doi = f"https://doi.org/{DOI_DATASET}" if DOI_DATASET else "(a ser emitido no Zenodo)"
    return f"""---
license: cc-by-4.0
language:
  - pt
tags:
  - synthetic
  - education
  - brazil
  - lgpd
  - inep
pretty_name: {TITULO}
size_categories:
  - 10K<n<100K
---

# {TITULO} v{DATASET_VERSION}

Dataset **inteiramente sintético** (procedural, LGPD-safe) de escolas, turmas e
alunos brasileiros, gerado pelo [SchoolMock-BR](https://github.com/RandMelville/schoolmock-br)
v{LIB_VERSION}. **Todos os registros são fictícios — não correspondem a pessoas reais.**

- **Escolas:** {contagens['escolas']} · **Turmas:** {contagens['turmas']} · **Alunos:** {contagens['alunos']}
- **Conformidade** (verificador C1–C5): alunos {conformidade['alunos']['taxa']:.0%}, escolas {conformidade['escolas']['taxa']:.0%}
- **Licença:** CC-BY 4.0 · **DOI:** {doi}
- **Reprodutível:** `python scripts/gerar_dataset_oficial.py` (seed={SEED}, schoolmock-br {LIB_VERSION})

## Arquivos

- `schoolmock-br-dataset.json` — dataset relacional único (escolas + turmas + alunos + metadados).
- `csv/escolas.csv`, `csv/turmas.csv`, `csv/alunos.csv` — uma tabela por entidade.
- `csv/metadata.json` — metadados e relatório de conformidade.
- `SHA256SUMS.txt` — checksums de integridade.

## Esquema

**escolas:** `nome_escola, codigo_inep, endereco, cidade, uf, rede, fonte`
**turmas:** `turma_id, codigo_inep, serie, turno, ano_letivo, qtd_alunos, fonte`
**alunos:** `turma_id, codigo_inep, nome_completo, cpf, data_nascimento, nome_mae, matricula, situacao, serie_atual, fonte`

Chaves: `codigo_inep` liga aluno/turma→escola; `turma_id` liga aluno→turma.
Garantias por construção: CPF válido (C1), INEP↔UF (C2), idade↔série (C3),
campos obrigatórios (C4) e unicidade de `codigo_inep`/`cpf`/`matricula` (C5).

## Aviso

Dado sintético **não** é dado pessoal (LGPD, art. 5º, I). Use livremente para
testes, ensino e pesquisa, citando o DOI acima.
"""


LICENSE_TXT = """Creative Commons Attribution 4.0 International (CC BY 4.0)

Copyright (c) 2026 Randerson Oliveira Melville Rebouças (PPGIE/UFRGS)

Você tem o direito de compartilhar e adaptar este material para qualquer
finalidade, inclusive comercial, desde que atribua o devido crédito (cite o DOI).

Texto legal completo: https://creativecommons.org/licenses/by/4.0/legalcode.pt
Resumo: https://creativecommons.org/licenses/by/4.0/deed.pt
"""


def _sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera o dataset oficial congelado.")
    parser.add_argument(
        "--out",
        default=str(_REPO / "dist-dataset"),
        help="Diretório de saída (default: dist-dataset/).",
    )
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    print(f"Gerando dataset v{DATASET_VERSION} com SchoolMock-BR v{LIB_VERSION} (seed={SEED})...")
    ds = construir_dataset(
        seed=SEED,
        n_escolas=N_ESCOLAS,
        turmas_por_escola=TURMAS_POR_ESCOLA,
        alunos_por_turma=ALUNOS_POR_TURMA,
        ano_letivo=ANO_LETIVO,
        verificar=True,
    )

    # Metadados do ARTEFATO (distintos dos metadados de geração da biblioteca):
    # fixam a data e acrescentam identidade, licença e proveniência citável.
    ds.metadata["gerado_em"] = DATA_GERACAO
    ds.metadata["dataset"] = {
        "titulo": TITULO,
        "versao": DATASET_VERSION,
        "autor": AUTOR,
        "licenca": LICENCA,
        "gerador": f"schoolmock-br {LIB_VERSION}",
        "parametros": {
            "seed": SEED,
            "n_escolas": N_ESCOLAS,
            "turmas_por_escola": list(TURMAS_POR_ESCOLA),
            "alunos_por_turma": list(ALUNOS_POR_TURMA),
            "ano_letivo": ANO_LETIVO,
        },
        "reproduzir": "python scripts/gerar_dataset_oficial.py",
    }

    # Export: JSON relacional único + CSVs por entidade (em subpastas).
    json_path = out / "schoolmock-br-dataset.json"
    ds.export_json(json_path)
    csv_dir = out / "csv"
    ds.export_csv(csv_dir)

    # Manifesto de checksums (SHA-256) de tudo que será publicado.
    artefatos = [json_path, *sorted(csv_dir.glob("*.csv")), csv_dir / "metadata.json"]
    sums_path = out / "SHA256SUMS.txt"
    linhas = [f"{_sha256(p)}  {p.relative_to(out)}" for p in artefatos]
    sums_path.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    c = ds.metadata["contagens"]
    conf = ds.metadata["conformidade"]

    # Documentação do pacote de publicação (não entra no manifesto de dados).
    (out / "README.md").write_text(_card_md(c, conf), encoding="utf-8")
    (out / "LICENSE").write_text(LICENSE_TXT, encoding="utf-8")
    print(f"  escolas={c['escolas']} turmas={c['turmas']} alunos={c['alunos']}")
    print(f"  conformidade alunos={conf['alunos']['taxa']} escolas={conf['escolas']['taxa']}")
    print(f"  JSON: {json_path}  ({json_path.stat().st_size / 1024:.0f} KB)")
    print(f"  CSV:  {csv_dir}/")
    print(f"  Checksums: {sums_path}")
    print(f"  Card+licença: {out / 'README.md'}, {out / 'LICENSE'}")
    print("OK.")


if __name__ == "__main__":
    main()
