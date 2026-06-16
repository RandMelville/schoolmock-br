from datetime import date

from schoolmock_br.baseline import SchoolMockBRv1
from schoolmock_br.verifier import Verificador

REF = date(2026, 6, 15)


def _verificador():
    return Verificador(data_referencia=REF)


def test_aluno_conforme_passa_todos_criterios():
    aluno = {
        "nome_completo": "Fulano de Tal",
        "cpf": "529.982.247-25",  # CPF válido conhecido em exemplos
        "data_nascimento": "13/03/2013",  # ~13 anos em 2026
        "serie_atual": "8º Ano",
        "matricula": "12345678",
    }
    rep = _verificador().verificar_aluno(aluno)
    assert rep.conforme, rep.violacoes


def test_c1_detecta_cpf_invalido():
    aluno = {
        "nome_completo": "X", "cpf": "111.111.111-11",
        "data_nascimento": "13/03/2013", "serie_atual": "8º Ano", "matricula": "1",
    }
    rep = _verificador().verificar_aluno(aluno)
    assert any(v.criterio == "C1" for v in rep.violacoes)


def test_c3_detecta_idade_incoerente():
    aluno = {
        "nome_completo": "X", "cpf": "529.982.247-25",
        "data_nascimento": "01/01/2020",  # 6 anos para um 8º ano -> incoerente
        "serie_atual": "8º Ano", "matricula": "1",
    }
    rep = _verificador().verificar_aluno(aluno)
    assert any(v.criterio == "C3" for v in rep.violacoes)


def test_c2_detecta_inep_uf_inconsistente():
    escola = {"nome_escola": "Y", "codigo_inep": "35000001", "uf": "RS"}  # 35 = SP
    rep = _verificador().verificar_escola(escola)
    assert any(v.criterio == "C2" for v in rep.violacoes)


def test_c2_aceita_inep_uf_consistente():
    escola = {"nome_escola": "Y", "codigo_inep": "43000001", "uf": "RS"}  # 43 = RS
    rep = _verificador().verificar_escola(escola)
    assert rep.conforme, rep.violacoes


def test_c4_detecta_campo_faltando():
    rep = _verificador().verificar_aluno({"cpf": "529.982.247-25"})
    assert any(v.criterio == "C4" for v in rep.violacoes)


def test_c5_detecta_matricula_duplicada():
    alunos = [
        {"nome_completo": "A", "cpf": "529.982.247-25", "data_nascimento": "13/03/2013",
         "serie_atual": "8º Ano", "matricula": "999"},
        {"nome_completo": "B", "cpf": "529.982.247-25", "data_nascimento": "13/03/2013",
         "serie_atual": "8º Ano", "matricula": "999"},
    ]
    rep = _verificador().verificar_lote_alunos(alunos)
    assert rep.violacoes_por_criterio.get("C5", 0) >= 1


def test_baseline_v1_tem_nao_conformidade_relevante():
    """O v1 ingênuo deve falhar em massa em C2 (INEP↔UF) e C3 (séries != 8/9)."""
    v1 = SchoolMockBRv1(seed=42)
    alunos = [v1.gerar_aluno(s) for s in ("5º Ano", "6º Ano", "7º Ano") for _ in range(20)]
    escolas = [v1.gerar_escola() for _ in range(50)]
    verif = _verificador()
    rep_alunos = verif.verificar_lote_alunos(alunos)
    rep_escolas = verif.verificar_lote_escolas(escolas)
    assert rep_alunos.violacoes_por_criterio.get("C3", 0) > 0
    assert rep_escolas.violacoes_por_criterio.get("C2", 0) > 0
