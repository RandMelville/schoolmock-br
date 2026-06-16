import random

from schoolmock_br.cpf import SEQUENCIAS_INVALIDAS, cpf_valido, gerar_cpf


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
