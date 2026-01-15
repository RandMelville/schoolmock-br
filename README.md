# SchoolMock-BR 🇧🇷

> **Micro-biblioteca para geração de dados educacionais sintéticos compatíveis com a LGPD e padrões do INEP.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Stable-green)]()

## 🎯 Objetivo

O **SchoolMock-BR** resolve o dilema de testar softwares educacionais sem violar a privacidade de estudantes reais. A ferramenta gera perfis de alunos, turmas e escolas que são **matematicamente válidos** (CPFs, Códigos INEP) mas **juridicamente seguros** (fictícios), permitindo conformidade total com a Lei Geral de Proteção de Dados (LGPD).

## Funcionalidades Principais

* **Validação de CPF (Módulo 11):** Gera documentos que passam em validações de backend e frontend governamentais.
* **Consistência Temporal:** Algoritmo heurístico que vincula a `Série Escolar` à `Data de Nascimento` provável (ex: Aluno do 8º ano com ~13 anos).
* **Padrão INEP/Censo:** Escolas geradas com código INEP de 8 dígitos e endereçamento brasileiro real.
* **Performance:** Arquitetura de métodos estáticos ("Zero-Instância") otimizada para gerar milhares de registros em segundos.

## Instalação

A biblioteca requer Python 3.10+ e o pacote `Faker`.

```bash
# 1. Clone o repositório
git clone [https://github.com/RandMelville/schoolmock-br.git](https://github.com/RandMelville/schoolmock-br.git)

# 2. Instale as dependências
pip install faker
