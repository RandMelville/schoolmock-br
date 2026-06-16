import pytest

from schoolmock_br.data.series import faixa_etaria_esperada


@pytest.mark.parametrize(
    "serie,idade",
    [
        ("1º Ano", 6),
        ("5º Ano", 10),
        ("8º Ano", 13),
        ("9º Ano", 14),
        ("oitavo ano", 13),
        ("1ª Série EM", 15),
        ("3ª série do ensino médio", 17),
    ],
)
def test_idade_adequada(serie, idade):
    faixa = faixa_etaria_esperada(serie)
    assert faixa is not None
    assert faixa[0] <= idade <= faixa[1]


def test_pre_escola_e_creche():
    assert faixa_etaria_esperada("Pré-escola") == (4, 5)
    assert faixa_etaria_esperada("Creche") == (0, 3)


def test_serie_desconhecida():
    assert faixa_etaria_esperada("qualquer coisa") is None
    assert faixa_etaria_esperada("") is None
