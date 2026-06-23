# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.
O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [2.1.0] — 2026-06-23

### Corrigido
- **Nomes sem pronome de tratamento.** O gerador deixava de antepor "Sr./Sra./
  Dr./Dra./Srta." aos nomes de alunos e mães. Esses pronomes (~16,5% dos
  registros) são irreais para um cadastro de crianças e adolescentes e não
  ocorrem no Censo Escolar. Os critérios de conformidade C1–C5 não são afetados.

### Notas
- Mudança de saída observável do `Gerador` (os nomes gerados para uma mesma
  semente mudam). O achado metodológico v1 vs v2 (baseado em C1–C5) permanece
  inalterado, pois não depende dos nomes.
- Esta é a versão sobre a qual o **dataset oficial congelado** é gerado.

## [2.0.0] — 2026-06-23

### Adicionado
- Primeira release estável (Production/Stable), publicada no PyPI
  (`pip install schoolmock-br`) e arquivada no Zenodo.
- `Gerador(seed=...)` reprodutível (F4); camada `Verificador` (C1–C5);
  `modo_teste` / `cpf_marcado_para_teste` (F3); construtor de dataset relacional
  (`construir_dataset`) com export JSON/CSV; CLI `schoolmock`.
- Enquadramento LGPD (dado sintético ≠ dado pessoal), `DATASHEET.md`
  (padrão Gebru et al.), CI (ruff + pytest 3.10–3.12).

[2.1.0]: https://github.com/RandMelville/schoolmock-br/releases/tag/v2.1.0
[2.0.0]: https://github.com/RandMelville/schoolmock-br/releases/tag/v2.0.0
