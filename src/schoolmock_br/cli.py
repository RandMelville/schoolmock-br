"""
Interface de linha de comando do SchoolMock-BR.

    schoolmock gerar --tipo aluno --n 10 --seed 42 [--formato json|csv] [--out arquivo]
    schoolmock verificar arquivo.json [--tipo aluno|escola]
    schoolmock benchmark [--seed 42]
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from datetime import date

from . import __version__
from .benchmark import formatar_relatorio, rodar_benchmark
from .core import Gerador
from .dataset import construir_dataset
from .verifier import Verificador


def _exportar(registros: list[dict], formato: str) -> str:
    if formato == "json":
        return json.dumps(registros, ensure_ascii=False, indent=2)
    buffer = io.StringIO()
    if registros:
        writer = csv.DictWriter(buffer, fieldnames=list(registros[0].keys()))
        writer.writeheader()
        writer.writerows(registros)
    return buffer.getvalue()


def _cmd_gerar(args: argparse.Namespace) -> int:
    gerador = Gerador(seed=args.seed, modo_teste=args.modo_teste)
    if args.tipo == "aluno":
        registros = gerador.gerar_turma_lote(qtd=args.n, serie=args.serie)
    else:
        registros = [gerador.gerar_escola() for _ in range(args.n)]
    saida = _exportar(registros, args.formato)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="") as fh:
            fh.write(saida)
        print(f"{len(registros)} registro(s) gravado(s) em {args.out}", file=sys.stderr)
    else:
        print(saida)
    return 0


def _cmd_verificar(args: argparse.Namespace) -> int:
    with open(args.arquivo, encoding="utf-8") as fh:
        registros = json.load(fh)
    if not isinstance(registros, list):
        registros = [registros]
    verificador = Verificador()
    if args.tipo == "escola":
        rep = verificador.verificar_lote_escolas(registros)
    else:
        rep = verificador.verificar_lote_alunos(registros)
    print(rep.resumo())
    return 0 if rep.nao_conformes == 0 else 1


def _cmd_benchmark(args: argparse.Namespace) -> int:
    data_ref = date.fromisoformat(args.data_referencia) if args.data_referencia else None
    resultados = rodar_benchmark(seed=args.seed, data_referencia=data_ref)
    print(formatar_relatorio(resultados))
    return 0


def _cmd_dataset(args: argparse.Namespace) -> int:
    ds = construir_dataset(seed=args.seed, n_escolas=args.escolas, modo_teste=args.modo_teste)
    if args.formato == "csv":
        destino = args.out or "dataset"
        escritos = ds.export_csv(destino)
        nomes = ", ".join(p.name for p in escritos)
        print(f"Dataset CSV gravado em {destino}/ ({nomes})", file=sys.stderr)
    else:
        destino = args.out or "dataset.json"
        ds.export_json(destino)
        print(f"Dataset JSON gravado em {destino}", file=sys.stderr)
    c = ds.metadata["contagens"]
    conf = ds.metadata.get("conformidade", {})
    print(f"  escolas={c['escolas']} turmas={c['turmas']} alunos={c['alunos']}", file=sys.stderr)
    if conf:
        ta = conf["alunos"]["taxa"]
        te = conf["escolas"]["taxa"]
        print(f"  conformidade: alunos={ta:.1%} escolas={te:.1%}", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="schoolmock", description="Dados educacionais sintéticos BR."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="comando", required=True)

    g = sub.add_parser("gerar", help="Gera registros sintéticos.")
    g.add_argument("--tipo", choices=["aluno", "escola"], default="aluno")
    g.add_argument("--n", type=int, default=10)
    g.add_argument("--serie", default="8º Ano")
    g.add_argument("--seed", type=int, default=None)
    g.add_argument("--formato", choices=["json", "csv"], default="json")
    g.add_argument("--out", default=None)
    g.add_argument(
        "--modo-teste", dest="modo_teste", action="store_true",
        help="Gera CPFs com prefixo sentinela, reconhecíveis como sintéticos (F3).",
    )
    g.set_defaults(func=_cmd_gerar)

    v = sub.add_parser("verificar", help="Verifica um arquivo JSON contra C1–C5.")
    v.add_argument("arquivo")
    v.add_argument("--tipo", choices=["aluno", "escola"], default="aluno")
    v.set_defaults(func=_cmd_verificar)

    b = sub.add_parser("benchmark", help="Compara conformidade v1 (ingênuo) vs v2.")
    b.add_argument("--seed", type=int, default=42)
    b.add_argument(
        "--data-referencia", dest="data_referencia", default=None, metavar="AAAA-MM-DD",
        help="Data de referência (ISO) para o critério idade↔série. "
             "Padrão: data fixa do benchmark, para reprodutibilidade.",
    )
    b.set_defaults(func=_cmd_benchmark)

    d = sub.add_parser("dataset", help="Constrói dataset relacional escola↔turma↔aluno.")
    d.add_argument("--escolas", type=int, default=10)
    d.add_argument("--seed", type=int, default=42)
    d.add_argument("--formato", choices=["json", "csv"], default="json")
    d.add_argument("--out", default=None, help="Arquivo (json) ou diretório (csv).")
    d.add_argument(
        "--modo-teste", dest="modo_teste", action="store_true",
        help="Gera CPFs com prefixo sentinela, reconhecíveis como sintéticos (F3).",
    )
    d.set_defaults(func=_cmd_dataset)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
