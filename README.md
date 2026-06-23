# SchoolMock-BR 🇧🇷

> **Gerador procedural de dados educacionais brasileiros sintéticos — realistas, mas fictícios — com camada de verificação determinística. Privacidade por construção (LGPD-safe).**

[![CI](https://github.com/RandMelville/schoolmock-br/actions/workflows/ci.yml/badge.svg)](https://github.com/RandMelville/schoolmock-br/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Stable%20(v2)-brightgreen)]()
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20806098.svg)](https://doi.org/10.5281/zenodo.20806098)

## 🎯 Objetivo

O **SchoolMock-BR** resolve o dilema de testar softwares educacionais administrativos sem
processar dados de estudantes reais. A ferramenta gera perfis de **alunos, turmas e escolas**
que são **estruturalmente válidos** (CPFs com dígito verificador correto, códigos INEP consistentes
com a UF, idade coerente com a série) mas **inteiramente fictícios** — não correspondem a nenhuma
pessoa real.

É um gerador **procedural por regras de domínio** (no espírito do [Synthea](https://synthetichealth.github.io/synthea/)
para a saúde): não aprende de dados reais, portanto **não há dado sensível a vazar**.

## ✨ Destaques do v2

* **Camada de verificação (C1–C5)** — um verificador determinístico que audita cada registro:
  CPF válido, INEP↔UF consistente, idade↔série coerente, campos obrigatórios e unicidade no lote.
* **Reprodutibilidade total** — `seed` propagada para `random` e `Faker`; o mesmo dataset, byte a byte.
* **Construtor de dataset relacional** — escola↔turma↔aluno com integridade referencial e export JSON/CSV.
* **CLI** — gere, verifique e exporte sem escrever Python.
* **Retrocompatível** — a API do v1 (`SchoolMockBR.gerar_aluno/gerar_escola/gerar_turma_lote`) continua válida.

## 📦 Instalação

Requer Python 3.10+.

```bash
pip install schoolmock-br        # quando publicado no PyPI
# ou, a partir do código-fonte:
git clone https://github.com/RandMelville/schoolmock-br.git
cd schoolmock-br
pip install -e ".[dev]"
```

## 🚀 Uso rápido

### Como biblioteca

```python
from schoolmock_br import Gerador, Verificador

gen = Gerador(seed=42)                      # reprodutível
aluno = gen.gerar_aluno("8º Ano")
escola = gen.gerar_escola()
turma = gen.gerar_turma_lote(qtd=30, serie="5º Ano")

verif = Verificador()
relatorio = verif.verificar_lote_alunos(turma)
print(relatorio.resumo())                   # conformidade C1–C5
```

A API estática do v1 segue funcionando (use `SchoolMockBR.semear(seed)` para reprodutibilidade):

```python
from schoolmock_br import SchoolMockBR
SchoolMockBR.semear(42)
aluno = SchoolMockBR.gerar_aluno("8º Ano")
```

### Pela linha de comando

```bash
schoolmock gerar --tipo aluno --n 30 --serie "5º Ano" --seed 42 --formato csv --out turma.csv
schoolmock verificar turma.json --tipo aluno
schoolmock dataset --escolas 50 --seed 42 --formato csv --out ./dataset
schoolmock benchmark --seed 42            # conformidade v1 (ingênuo) vs v2
```

## 🔍 A camada de verificação (critérios C1–C5)

| Critério | Verifica |
|---|---|
| **C1** | CPF válido (mód-11) e não pertencente a sequências conhecidas-inválidas |
| **C2** | Código INEP consistente com a UF (2 primeiros dígitos = código IBGE da UF) |
| **C3** | Idade coerente com a série (data de nascimento ↔ série, idade adequada) |
| **C4** | Campos obrigatórios presentes e não vazios |
| **C5** | Unicidade de identificadores no lote (`cpf`, `matricula`, `codigo_inep`) |

O verificador é **determinístico**: mesma entrada e mesma `data_referencia` → mesmo veredito.
Rodá-lo sobre o gerador ingênuo (v1) e sobre o v2 produz o contraste de conformidade
(`schoolmock benchmark`): o v1 gera dezenas de % de registros não-conformes (idade↔série,
INEP↔UF); o v2 garante **100% de conformidade por construção**.

## 🗂️ Construtor de dataset

```python
from schoolmock_br.dataset import construir_dataset

ds = construir_dataset(seed=42, n_escolas=50)
ds.export_csv("dataset/")        # escolas.csv, turmas.csv, alunos.csv, metadata.json
```

Cada registro carrega o campo `fonte` (marcação de origem sintética) e os metadados incluem
`seed`, contagens e o resumo de conformidade. Veja o **[DATASHEET.md](DATASHEET.md)** para a
documentação completa no padrão *Datasheets for Datasets* (Gebru et al., 2018).

## ⚖️ Enquadramento legal (LGPD)

Os registros gerados são **dados sintéticos**: produzidos proceduralmente, **não se referem a
pessoa natural identificada ou identificável**. Pela definição de dado pessoal da
[LGPD (Lei nº 13.709/2018, art. 5º, I)](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm),
dados que não se vinculam a uma pessoa real **não constituem dado pessoal** — logo, o regime de
tratamento da LGPD (incluindo o consentimento do art. 14, relativo a crianças e adolescentes)
**não incide sobre os registros sintéticos em si**.

O valor da ferramenta é justamente apoiar os princípios de **necessidade e minimização**
(art. 6º) e a **privacidade desde a concepção** (*privacy by design*): ao testar sistemas
educacionais com dados fictícios em vez de dados reais de estudantes, evita-se o tratamento de
dados pessoais de menores onde ele não é necessário.

> ⚠️ **Não** use o SchoolMock-BR para "contornar" o consentimento sobre dados reais. A premissa é
> não haver dado real envolvido. Se você cruzar, enriquecer ou vincular esses registros a dados de
> pessoas reais, o resultado passa a ser dado pessoal e a LGPD volta a incidir.

## ⚠️ Limitações honestas

* **Fidelidade estatística.** O gerador garante validade *estrutural*, não reproduz as
  distribuições reais de uma população (proporções por rede/UF/série). Calibração contra marginais
  públicas do Censo Escolar é um trabalho futuro (F7 no roadmap).
* **Risco residual de colisão de CPF.** Um CPF sintético, embora fictício, pode por coincidência
  coincidir com o de uma pessoa real (o espaço de CPFs válidos é finito e não há faixa oficial de
  teste). Não use os identificadores para nenhuma finalidade que pressuponha titularidade real.
  O modo opcional `--modo-teste` (F3) fixa um prefixo sentinela (`999…`) nos CPFs, tornando-os
  reconhecíveis como sintéticos (`cpf_marcado_para_teste()`) — mitigação por *detectabilidade*,
  não garantia de não-colisão.
* **Escopo administrativo.** A ferramenta foi pensada para testes de software educacional
  administrativo (cadastros, carga, conformidade), não como corpus de treinamento de modelos.

## 🧪 Desenvolvimento

```bash
pip install -e ".[dev]"
pytest            # suíte de testes (a camada de verificação é parte dela)
ruff check src tests
```

## 📚 Como citar

Se este trabalho for útil em sua pesquisa, cite o software via o **DOI conceitual** do Zenodo
([10.5281/zenodo.20806098](https://doi.org/10.5281/zenodo.20806098) — resolve sempre para a versão
mais recente) ou use o arquivo [`CITATION.cff`](CITATION.cff). Para citar especificamente a
**v2.0.0**, use o DOI desta versão
([10.5281/zenodo.20806099](https://doi.org/10.5281/zenodo.20806099)). O Manual Técnico v1 está
registrado sob o ISBN 978-65-01-89921-3 (DOI
[10.5281/zenodo.18343467](https://doi.org/10.5281/zenodo.18343467)).

## 📄 Licença

Código sob licença [MIT](LICENSE). O dataset sintético publicado é distribuído sob **CC-BY 4.0**.

---

Autor: **Randerson Oliveira Melville Rebouças** (PPGIE/UFRGS).
