from schoolmock_br import Gerador, SchoolMockBR


def test_seed_reprodutivel():
    a = Gerador(seed=123).gerar_turma_lote(qtd=5)
    b = Gerador(seed=123).gerar_turma_lote(qtd=5)
    assert a == b


def test_seeds_diferentes_produzem_resultados_diferentes():
    a = Gerador(seed=1).gerar_aluno()
    b = Gerador(seed=2).gerar_aluno()
    assert a != b


def test_api_retrocompativel_estatica():
    aluno = SchoolMockBR.gerar_aluno("8º Ano")
    assert set(aluno) >= {"nome_completo", "cpf", "data_nascimento", "serie_atual", "matricula"}
    escola = SchoolMockBR.gerar_escola()
    assert set(escola) >= {"nome_escola", "codigo_inep", "uf"}
    assert len(SchoolMockBR.gerar_turma_lote(3)) == 3


def test_facade_semear():
    SchoolMockBR.semear(99)
    primeiro = SchoolMockBR.gerar_aluno()
    SchoolMockBR.semear(99)
    assert SchoolMockBR.gerar_aluno() == primeiro
