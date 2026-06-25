---
title: 'SchoolMock-BR: A rule-based generator of synthetic Brazilian educational data with a deterministic verification layer'
tags:
  - Python
  - synthetic data
  - education
  - Brazil
  - LGPD
  - reproducibility
  - software testing
authors:
  - name: Randerson Oliveira Melville Rebouças
    orcid: 0000-0000-0000-0000  # TODO: preencher ORCID real
    affiliation: 1
affiliations:
  - index: 1
    name: Programa de Pós-Graduação em Informática na Educação (PPGIE), Universidade Federal do Rio Grande do Sul (UFRGS), Brazil
    # ror: 041yk2d64  # TODO: confirmar ROR da UFRGS antes de submeter
date: 25 June 2026
bibliography: paper.bib
---

# Summary

`SchoolMock-BR` is a Python library and command-line tool that generates synthetic
Brazilian educational records — students, classes and schools — that are
*structurally valid* yet entirely fictitious. Records are produced procedurally
from domain rules rather than learned from real data, in the spirit of rule-based
generators such as Synthea for healthcare [@walonoski2018synthea]. Each record
carries Brazil-specific structure: CPF identifiers with valid check digits, INEP
school codes consistent with the federative unit (UF), and birth dates coherent
with the school grade.

The distinguishing feature of the software is a **deterministic verification
layer** that audits every generated record against five criteria (C1–C5): valid
CPF (mod-11), INEP↔UF consistency, age↔grade coherence, presence of required
fields, and uniqueness of identifiers within a batch. Generation is deterministic:
a single `seed` is propagated to both `random` and `Faker` [@faker], making any
dataset byte-for-byte reproducible for a fixed software version. The package also
ships a relational dataset builder (school↔class↔student with referential
integrity), a CLI (`schoolmock gerar | verificar | benchmark | dataset`), and a
frozen reimplementation of the original v1 generator that serves as an immutable
scientific baseline. The software is distributed on PyPI (`pip install
schoolmock-br`) and archived on Zenodo under a concept DOI [@schoolmock_software].

# Statement of need

Educational research and teaching in Brazil require microdata, but two obstacles
recur. First, real student data falls under the Brazilian General Data Protection
Law (LGPD, Lei nº 13.709/2018) [@lgpd2018], which is especially restrictive for
data on children and adolescents; using real records to test administrative
education software is therefore often neither necessary nor advisable. Second,
naively generated synthetic data is frequently *structurally inconsistent*
(e.g., a student's age incompatible with the declared grade, or an INEP code that
does not match the federative unit), and rarely reproducible — which undermines
its use both as a controlled test fixture and as a shareable research artifact.

`SchoolMock-BR` addresses both. Because records do not refer to any identified or
identifiable natural person, they fall outside the LGPD's definition of personal
data, supporting *privacy by design* and the principles of necessity and
minimization when testing administrative education systems (record loading,
registration, conformance checks). Crucially, the software does not assume that
*generating* data is the same as *guaranteeing* its validity: a separate,
deterministic verification layer makes structural conformance an explicit,
auditable step. The intended users are researchers and educators who need
LGPD-safe fixtures for educational software, and developers of administrative
education systems who need reproducible, structurally valid test data.

# State of the field

General-purpose fake-data libraries such as Faker [@faker] produce locale-aware
values (names, addresses, Brazilian CPF strings) but model neither the domain
relationships between fields nor their validity: a Faker-generated record can pair
an INEP code with the wrong state, or a birth date with an incongruent grade, and
nothing flags it. Rule-based clinical generators such as Synthea
[@walonoski2018synthea] demonstrate the value of procedural, domain-constrained
generation that learns from no real patient, but they target the U.S. healthcare
domain and do not encode Brazilian educational structure. Documentation standards
such as *Datasheets for Datasets* [@gebru2021datasheets] address how a dataset
should be described, not how it should be generated or validated.

To our knowledge, no open-source package generates Brazilian educational microdata
that is simultaneously domain-consistent (CPF, INEP↔UF, age↔grade), reproducible
by seed, and *verified* by an explicit conformance layer. Extending Faker would
not suffice: the missing component is not more realistic field values but the
relational rules and the verifier that enforce and audit them. `SchoolMock-BR`
therefore contributes a new, domain-specific package rather than a plugin to an
existing one.

# Software design

The package separates two concerns that naive generators conflate. The `Gerador`
component (`core.py`) produces records from procedural domain rules, drawing
locale values from Faker and seeding both `random` and `Faker` from a single
`seed` for reproducibility. The independent `Verificador` component
(`verifier.py`) audits any batch of records — whatever their origin — against the
deterministic criteria C1–C5, encoded from external references: CPF check digits
(`cpf.py`), IBGE/UF prefixes for INEP codes (`data/ibge.py`), and grade-to-age
tables (`data/series.py`). Because the verifier is deterministic, the same input
and reference date always yield the same verdict, which makes conformance testable
and the headline benchmark reproducible.

A faithful reimplementation of the original v1 generator (`baseline.py`) is
preserved as an immutable control and excluded from linting, so the structural
defects it exhibits cannot be silently "fixed"; this enables a reproducible
before/after comparison (`benchmark.py`). A relational dataset builder
(`dataset.py`) composes verified records into school↔class↔student structures with
referential integrity and Datasheets-style metadata, and a thin CLI (`cli.py`)
exposes generation, verification, benchmarking, and dataset export. The central
design trade-off is deliberate: the tool guarantees *structural* validity, not
statistical fidelity to real population marginals (rede/UF/grade proportions);
calibration against public Census marginals is explicit future work. Rule-based
generation was chosen over learning from real data precisely so that no sensitive
data is ingested and none can leak — privacy holds by construction.

# Research impact statement

The software underpins a frozen, citable reference dataset published on Zenodo
[@schoolmock_dataset] (100 schools, 450 classes, 12,505 students; CC-BY 4.0),
and a technical manual registered under ISBN 978-65-01-89921-3, giving the work
persistent, independently citable artifacts. The verification layer yields a
concrete, reproducible benchmark: under a fixed reference date (2026-06-15) and
the default sample (600 student and 200 school records), the frozen v1 generator
produces only 32.5% conformant student records (failing the age↔grade criterion
C3) and 2.0% conformant school records (failing the INEP↔UF criterion C2),
whereas the verified v2 reaches 100% conformance for both by construction —
demonstrating, with an auditable control, that generation without verification
silently emits structurally invalid data. The package is released on PyPI, is
versioned, and runs continuous integration across Python 3.10–3.12, signalling
community-readiness for adoption as a testing and teaching fixture.
<!-- TODO (autor): se houver, inserir aqui evidência concreta e específica de uso
externo — nº de downloads PyPI/Zenodo, trabalhos/disciplinas que já usam o
dataset — pois o JOSS exige impacto demonstrado, não aspiracional. -->

# AI usage disclosure

Generative AI tools (Anthropic Claude, via the Claude Code CLI) were used to
assist with portions of the software engineering and the preparation of this
manuscript — including code refactoring, test scaffolding, documentation, and
drafting and copy-editing of the paper text. All scientific framing, the
domain rules and verification criteria (C1–C5), the experimental design, and the
interpretation of results were determined by the author, who reviewed, edited, and
validated every AI-assisted output and made all core design decisions. The author
is solely responsible for the accuracy, originality, licensing, and legal and
ethical compliance of the software and the paper.
<!-- TODO (autor): confirmar/ajustar as ferramentas, versões e o escopo exato
acima de modo que reflita fielmente o seu uso real antes de submeter. -->

# Acknowledgements

This work was developed within the PPGIE/UFRGS doctoral program.
<!-- TODO (autor): declarar explicitamente o apoio financeiro — ex.: bolsa
CAPES/CNPq (com nº de processo) — ou afirmar que não houve financiamento
específico. O JOSS exige o reconhecimento de qualquer apoio financeiro. -->
The synthetic dataset is released under CC-BY 4.0 and the software under the MIT
license.

# References
