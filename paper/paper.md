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
  - name: Programa de Pós-Graduação em Informática na Educação (PPGIE), Universidade Federal do Rio Grande do Sul (UFRGS), Brazil
    index: 1
date: 25 June 2026
bibliography: paper.bib
---

# Summary

`SchoolMock-BR` is a Python library and command-line tool that generates synthetic
Brazilian educational records — students, classes and schools — that are
*structurally valid* yet entirely fictitious. Records are produced procedurally
from domain rules rather than learned from real data, in the spirit of rule-based
generators such as Synthea for healthcare [@walonoski2018synthea]. Each record
carries Brazilian-specific structure: CPF identifiers with valid check digits,
INEP school codes consistent with the state (UF), and birth dates coherent with
the school grade.

The distinguishing feature of the software is a **deterministic verification
layer** that audits every generated record against five criteria (C1–C5): valid
CPF (mod-11), INEP↔UF consistency, age↔grade coherence, presence of required
fields, and uniqueness of identifiers within a batch. Generation is deterministic:
a single `seed` is propagated to both `random` and `Faker` [@faker], making any
dataset byte-for-byte reproducible for a fixed software version. The package also
ships a relational dataset builder (school↔class↔student with referential
integrity) and a CLI (`schoolmock gerar | verificar | benchmark | dataset`) that
exposes generation, verification and export (JSON/CSV) without writing Python.

The software is distributed on PyPI (`pip install schoolmock-br`) and archived on
Zenodo under a concept DOI [@schoolmock_software]. Its synthetic output is
documented following the *Datasheets for Datasets* methodology
[@gebru2021datasheets], and a frozen, citable dataset release accompanies it
[@schoolmock_dataset].

# Statement of need

Educational research and teaching in Brazil require microdata, but two obstacles
recur. First, real student data falls under the Brazilian General Data Protection
Law (LGPD, Lei nº 13.709/2018) [@lgpd2018], which is especially restrictive for
data on children and adolescents; using real records to test administrative
education software is therefore often neither necessary nor advisable. Second,
naively generated synthetic data is frequently *structurally inconsistent*
(e.g., a student's age incompatible with the declared grade, or an INEP code that
does not match the state), and rarely reproducible — which undermines its use both
as a controlled test fixture and as a shareable research artifact.

`SchoolMock-BR` addresses both. Because records do not refer to any identified or
identifiable natural person, they fall outside the LGPD's definition of personal
data, supporting *privacy by design* and the principles of necessity and
minimization when testing administrative education systems (record loading,
registration, conformance checks). Crucially, the software does not assume that
*generating* data is the same as *guaranteeing* its validity: the verification
layer makes structural conformance an explicit, auditable, deterministic step.
The bundled benchmark (`schoolmock benchmark --seed 42`) contrasts a faithful
reimplementation of the naive v1 generator with the verified v2. On a fixed
reference date (2026-06-15) and the default sample (600 student and 200 school
records), the naive generator yields 32.5% conformant student records (failing
the age↔grade criterion C3) and 2.0% conformant school records (failing the
INEP↔UF criterion C2), whereas the verified generator reaches 100% conformance
for both by construction.

The intended users are researchers and educators who need LGPD-safe fixtures for
educational software, and developers of administrative education systems who need
reproducible, structurally valid test data. The frozen v1 generator is preserved
in the repository as an immutable scientific baseline, enabling the before/after
comparison to be reproduced by anyone.

# Acknowledgements

This work was developed within the PPGIE/UFRGS doctoral program. The synthetic
dataset is released under CC-BY 4.0 and the software under the MIT license.

# References
