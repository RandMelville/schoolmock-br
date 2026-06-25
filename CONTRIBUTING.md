# Contribuindo com o SchoolMock-BR

Obrigado pelo interesse em contribuir. Este documento descreve como contribuir
com código, como relatar problemas e como obter suporte.

## Relatar bugs e pedir ajuda (issues / suporte)

- **Bugs e dúvidas de uso:** abra uma *issue* em
  <https://github.com/RandMelville/schoolmock-br/issues>. Inclua a versão
  (`schoolmock --version`), o sistema operacional, a versão do Python e um exemplo
  mínimo que reproduza o problema (de preferência com a `--seed` usada).
- **Suporte:** o canal de suporte é o rastreador de *issues* do GitHub. Não há
  lista de e-mail privada; perguntas em *issues* públicas ajudam outras pessoas.
- **Vulnerabilidades de segurança:** prefira contato direto com o autor
  (randerson.melville@gmail.com) antes de divulgar publicamente.

## Contribuir com código

1. Faça um *fork* e crie uma branch a partir de `main`.
2. Instale o ambiente de desenvolvimento:
   ```bash
   pip install -e ".[dev]"
   ```
3. Faça suas mudanças. Mantenha o escopo do projeto: geração **e verificação**
   determinística de dados educacionais BR sintéticos (LGPD-safe).
4. Garanta que a suíte passa e o lint está limpo:
   ```bash
   pytest                      # testes (a camada de verificação faz parte deles)
   ruff check src tests        # estilo/lint
   ```
   > ⚠️ Não altere `schoolmock_br.py` na raiz: é o **v1 congelado** (baseline
   > científico imutável), excluído do lint de propósito.
5. Abra um *pull request* descrevendo a motivação e a mudança. Inclua testes para
   comportamento novo; mudanças que afetem os números do benchmark devem atualizar
   `tests/test_conformidade.py` e o paper.

## Padrões

- Código formatado/lintado com `ruff` (config em `pyproject.toml`).
- Python 3.10+; CI roda em 3.10, 3.11 e 3.12.
- Mensagens de commit no estilo convencional (`feat:`, `fix:`, `docs:`, `test:`).

## Código de conduta

Espera-se interação respeitosa e colaborativa. Comportamento abusivo ou
assédio não serão tolerados; relate ao autor pelo e-mail acima.
