import random

from schoolmock_br.cpf import (
    PREFIXO_TESTE,
    SEQUENCIAS_INVALIDAS,
    apenas_digitos,
    cpf_marcado_para_teste,
    cpf_valido,
    gerar_cpf,
)


def test_cpf_gerado_eh_valido():
    rng = random.Random(0)
    for _ in range(500):
        assert cpf_valido(gerar_cpf(rng))


def test_rejeita_sequencias_repetidas():
    for seq in SEQUENCIAS_INVALIDAS:
        assert not cpf_valido(seq)


def test_rejeita_tamanho_e_dv_errados():
    assert not cpf_valido("123")
    assert not cpf_valido("123.456.789-00")


def test_geracao_seedada_eh_reprodutivel():
    assert gerar_cpf(random.Random(7)) == gerar_cpf(random.Random(7))


# --- F3: modo "marcado para teste" -------------------------------------------

def test_modo_teste_gera_cpf_valido_e_com_prefixo():
    rng = random.Random(0)
    for _ in range(500):
        cpf = gerar_cpf(rng, modo_teste=True)
        assert cpf_valido(cpf)  # C1 continua passando
        assert apenas_digitos(cpf).startswith(PREFIXO_TESTE)
        assert cpf_marcado_para_teste(cpf)


def test_cpf_normal_nao_eh_marcado_para_teste():
    # CPF sem o prefixo sentinela não é detectado como de teste.
    assert not cpf_marcado_para_teste("123.456.789-09")


def test_marcado_para_teste_exige_validade():
    # Mesmo começando com o prefixo, um CPF inválido não conta como marcado.
    invalido = PREFIXO_TESTE + "0000000-00"
    assert not cpf_marcado_para_teste(invalido)


def test_modo_teste_seedado_eh_reprodutivel():
    a = gerar_cpf(random.Random(7), modo_teste=True)
    b = gerar_cpf(random.Random(7), modo_teste=True)
    assert a == b
