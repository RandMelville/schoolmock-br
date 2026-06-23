# Dataset oficial de referência

Além da biblioteca (que gera dados sob demanda), o SchoolMock-BR publica um
**dataset congelado e citável** — uma fotografia fixa, com DOI, para que
resultados sejam comparáveis e reproduzíveis entre trabalhos.

O dataset **não** é versionado no Git: o repositório guarda apenas a *receita*
([`scripts/gerar_dataset_oficial.py`](scripts/gerar_dataset_oficial.py)), e o
artefato é distribuído no Zenodo (cópia citável) e espelhado no Hugging Face.

## Parâmetros congelados (dataset v1.0.0)

| Parâmetro | Valor |
|---|---|
| Biblioteca | `schoolmock-br` 2.1.0 |
| Seed | `2026` |
| Escolas | 100 |
| Turmas por escola | 3–6 |
| Alunos por turma | 20–35 |
| Ano letivo | 2026 |
| **Totais** | **100 escolas · 450 turmas · 12.505 alunos** |
| Conformidade (C1–C5) | alunos 100% · escolas 100% |
| Licença | CC-BY 4.0 |

> A seed `2026` é dedicada ao dataset. O `42` permanece reservado ao benchmark
> metodológico (`schoolmock benchmark --seed 42`), para não confundir "o número
> do achado" com "o número do dataset".

## Como (re)gerar e verificar

```bash
pip install schoolmock-br==2.1.0     # ou: pip install -e . no repositório
python scripts/gerar_dataset_oficial.py        # gera em dist-dataset/
cd dist-dataset && shasum -a 256 -c SHA256SUMS.txt   # confere integridade
```

A geração é **determinística**: mesma versão da biblioteca + mesma seed ⇒
artefato idêntico byte-a-byte. Os checksums abaixo são a referência oficial.

## Checksums oficiais (SHA-256)

```
c019ce8572ef5028a79205f74d3ca1649cc5e0bba14a658feba6af07216a2f85  schoolmock-br-dataset.json
541e25fb8105c7691bb72c841ae7a8eeba64533434c6bf3ce4687a4445861130  csv/alunos.csv
94d6876818ac9e8d17d994c539a73698a847978df716d199f6fe55d4b37e2bdd  csv/escolas.csv
21613f4d4e322572898053272e14e5ee449bf8d8a2bc60f5949ff3b40d9826c8  csv/turmas.csv
0536843f09fee57d16bc4b1b53c3c2e086f1135ad0e4c30408ae31051d191add  csv/metadata.json
```

## Esquema

- **escolas:** `nome_escola, codigo_inep, endereco, cidade, uf, rede, fonte`
- **turmas:** `turma_id, codigo_inep, serie, turno, ano_letivo, qtd_alunos, fonte`
- **alunos:** `turma_id, codigo_inep, nome_completo, cpf, data_nascimento, nome_mae, matricula, situacao, serie_atual, fonte`

`codigo_inep` liga aluno/turma → escola; `turma_id` liga aluno → turma.

## Publicação

| Onde | Papel | Referência |
|---|---|---|
| Zenodo | Primário (DOI, preservação, CC-BY) | _a preencher após reservar o DOI_ |
| Hugging Face | Espelho (`load_dataset`, descoberta) | _a preencher_ |

Linkar o record do dataset ao do software (`is supplement to`,
[10.5281/zenodo.20806098](https://doi.org/10.5281/zenodo.20806098)) e ao Manual
Técnico ([10.5281/zenodo.18343467](https://doi.org/10.5281/zenodo.18343467)).

## Natureza dos dados

Todos os registros são **fictícios**, gerados proceduralmente. Dado sintético
não é dado pessoal (LGPD, art. 5º, I); ver [`DATASHEET.md`](DATASHEET.md).
