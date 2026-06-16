# Datasheet — SchoolMock-BR (dados educacionais sintéticos)

Documentação no padrão **Datasheets for Datasets** (Gebru et al., 2018, arXiv:1803.09010),
referente ao dataset sintético produzido pelo gerador SchoolMock-BR v2.

> **Aviso central:** todos os registros deste dataset são **fictícios** e gerados
> **proceduralmente** por regras de domínio. Nenhum registro corresponde, ou pretende
> corresponder, a uma pessoa real. Não há fonte de dados reais por trás deles.

---

## 1. Motivação

**Para qual finalidade o dataset foi criado?**
Para permitir o teste de software educacional administrativo brasileiro (sistemas de matrícula,
cadastro de alunos, validação de documentos, testes de carga, verificação de conformidade) **sem
processar dados pessoais de estudantes reais**. Sistemas educacionais lidam majoritariamente com
dados de crianças e adolescentes; testá-los com dados reais é desnecessário e juridicamente
sensível. O dataset oferece uma alternativa estruturalmente válida e privada por construção.

**Quem criou e financiou?**
Randerson Oliveira Melville Rebouças (PPGIE — Programa de Pós-Graduação em Informática na Educação,
UFRGS). Trabalho independente, derivado do registro v1 (ISBN 978-65-01-89921-3, DOI Zenodo
10.5281/zenodo.18343467).

## 2. Composição

**O que cada instância representa?**
Três entidades relacionais vinculadas:
- **Escola** — `nome_escola`, `codigo_inep` (8 dígitos; 2 primeiros = código IBGE da UF), `endereco`,
  `cidade`, `uf`, `rede`, `fonte`.
- **Turma** — `turma_id`, `codigo_inep` (FK para escola), `serie`, `turno`, `ano_letivo`,
  `qtd_alunos`, `fonte`.
- **Aluno** — `turma_id` e `codigo_inep` (FKs), `nome_completo`, `cpf`, `data_nascimento`,
  `nome_mae`, `matricula`, `situacao`, `serie_atual`, `fonte`.

**Quantas instâncias?** Parametrizável (`construir_dataset(n_escolas=..., ...)`). Os metadados de
cada dataset registram as contagens efetivas.

**O dataset contém todas as instâncias possíveis ou é uma amostra?** É uma amostra gerada; o espaço
de instâncias possíveis é combinatorialmente grande. A amostragem é controlada por `seed`.

**Há rótulos/alvos?** Não. Não é um dataset de aprendizado supervisionado; é um corpus de teste.

**Falta informação em alguma instância?** Não — o critério C4 garante campos obrigatórios presentes.

**Relações explícitas entre instâncias?** Sim: integridade referencial escola→turma→aluno via
`codigo_inep` e `turma_id`.

**Há ruído, erros ou redundância?** Por construção, não: o verificador (C1–C5) garante 100% de
conformidade estrutural e unicidade de identificadores no lote.

**O dataset contém dados confidenciais ou pessoais?** **Não.** Os dados são sintéticos e não se
referem a pessoa natural identificável (ver seção 6, considerações legais).

## 3. Processo de coleta

**Como os dados foram adquiridos?** Não foram coletados; foram **gerados proceduralmente**. Nomes e
endereços usam a biblioteca `Faker` (locale `pt_BR`); CPFs são calculados com dígito verificador
mód-11; códigos INEP são compostos pelo código IBGE da UF + sufixo aleatório; a idade é derivada de
uma tabela canônica série→faixa etária (idade adequada da Educação Básica).

**Quem coletou e como foi a amostragem?** Geração determinística a partir de uma `seed`. Não há
sujeitos humanos, portanto não há consentimento, compensação ou revisão ética aplicáveis.

**Período de coleta.** N/A (geração sob demanda). Os metadados registram a data de geração.

## 4. Pré-processamento / limpeza / rotulagem

**Houve pré-processamento?** Não no sentido tradicional. A "limpeza" é substituída pela **camada de
verificação** (C1–C5), que valida cada registro no momento da geração. Registros não-conformes não
são produzidos pelo v2.

**Os dados brutos foram preservados?** O processo é reprodutível a partir da `seed` e da versão do
gerador, dispensando armazenamento de "brutos".

## 5. Usos

**Para que o dataset já foi/pode ser usado?**
- Testes funcionais e de carga de sistemas de cadastro/matrícula.
- Validação de rotinas de checagem de CPF e código INEP.
- Demonstrações e materiais didáticos sem expor dados reais.
- Evidência empírica de pesquisa (contraste de conformidade gerador ingênuo vs verificado).

**Há algo na composição que afete usos futuros?** Sim: o dataset **não reproduz distribuições
estatísticas reais** (ver Limitações). Não deve ser usado para inferência populacional nem como
corpus de treinamento que pressuponha realismo distribucional, salvo calibração futura (F7).

**Há usos para os quais NÃO deve ser utilizado?** Não deve ser vinculado/cruzado com dados de
pessoas reais; não deve ser apresentado como dado real; identificadores não devem ser usados para
finalidades que pressuponham titularidade real.

## 6. Distribuição e considerações legais

**Como será distribuído e sob qual licença?** Código sob **MIT**; dataset sob **CC-BY 4.0**;
publicação com DOI no Zenodo.

**Considerações legais (LGPD).** Por se referirem a pessoas fictícias, os registros **não constituem
dado pessoal** na acepção do art. 5º, I, da Lei nº 13.709/2018 (LGPD); o regime de tratamento — e a
exigência de consentimento do art. 14, sobre dados de crianças e adolescentes — **não incide sobre
os registros sintéticos**. A ferramenta apoia os princípios de necessidade e minimização (art. 6º).
**Risco residual:** um CPF sintético pode, por coincidência, coincidir com o de uma pessoa real;
trate os identificadores como fictícios e não os associe a titulares reais.

## 7. Manutenção

**Quem mantém?** O autor (contato no repositório).
**Como serão comunicadas atualizações?** Via versões do pacote e novas versões do registro Zenodo
(que herdam o histórico do DOI). O v1 permanece congelado como linha de base.
**Erratas/contribuições.** Via *issues* e *pull requests* no repositório GitHub.

---

*Referência do padrão:* Gebru, T. et al. (2018). *Datasheets for Datasets.* arXiv:1803.09010.
