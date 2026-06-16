import json

from schoolmock_br.dataset import construir_dataset


def _dataset():
    return construir_dataset(
        seed=7, n_escolas=5, turmas_por_escola=(2, 3), alunos_por_turma=(10, 15)
    )


def test_reprodutivel_com_seed():
    a = construir_dataset(seed=7, n_escolas=3).to_dict()
    b = construir_dataset(seed=7, n_escolas=3).to_dict()
    assert a == b


def test_estrutura_relacional_consistente():
    ds = _dataset()
    ineps = {e["codigo_inep"] for e in ds.escolas}
    turma_ids = {t["turma_id"] for t in ds.turmas}
    # toda turma referencia uma escola existente
    assert all(t["codigo_inep"] in ineps for t in ds.turmas)
    # todo aluno referencia turma e escola existentes
    assert all(a["turma_id"] in turma_ids for a in ds.alunos)
    assert all(a["codigo_inep"] in ineps for a in ds.alunos)


def test_identificadores_unicos_no_lote():
    ds = _dataset()
    cpfs = [a["cpf"] for a in ds.alunos]
    matriculas = [a["matricula"] for a in ds.alunos]
    ineps = [e["codigo_inep"] for e in ds.escolas]
    assert len(cpfs) == len(set(cpfs))
    assert len(matriculas) == len(set(matriculas))
    assert len(ineps) == len(set(ineps))


def test_marca_origem_sintetica():
    ds = _dataset()
    assert all("sintétic" in a["fonte"].lower() for a in ds.alunos)
    assert "aviso" in ds.metadata


def test_dataset_e_100_porcento_conforme():
    ds = _dataset()
    conf = ds.metadata["conformidade"]
    assert conf["alunos"]["taxa"] == 1.0
    assert conf["escolas"]["taxa"] == 1.0


def test_aluno_herda_serie_da_turma():
    ds = _dataset()
    serie_por_turma = {t["turma_id"]: t["serie"] for t in ds.turmas}
    assert all(a["serie_atual"] == serie_por_turma[a["turma_id"]] for a in ds.alunos)


def test_export_json(tmp_path):
    ds = _dataset()
    caminho = ds.export_json(tmp_path / "ds.json")
    carregado = json.loads(caminho.read_text(encoding="utf-8"))
    assert set(carregado) == {"metadata", "escolas", "turmas", "alunos"}


def test_export_csv(tmp_path):
    ds = _dataset()
    escritos = ds.export_csv(tmp_path / "saida")
    nomes = {p.name for p in escritos}
    assert {"escolas.csv", "turmas.csv", "alunos.csv", "metadata.json"} <= nomes
