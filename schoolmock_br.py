"""
SchoolMock-BR - Gerador de Dados Educacionais Brasileiros
---------------------------------------------------------
Autor: Randerson Oliveira Melville Rebouças
Data: 2026
Versão: 1.0 (Versão para Registro INPI)
Licença: MIT

Descrição:
Micro-Biblioteca para geração de dados sintéticos (fictícios) para testes de software
educacional, respeitando a LGPD e os padrões do Censo Escolar/INEP.
"""

import random
from datetime import date, timedelta
from faker import Faker

# Configuração inicial
fake = Faker('pt_BR')

class SchoolMockBR:
    """
    Classe principal para geração de dados educacionais sintéticos.
    """

    @staticmethod
    def _gerar_cpf_valido():
        """Gera um número de CPF matematicamente válido."""
        cpf = [random.randint(0, 9) for _ in range(9)]

        for _ in range(2):
            val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11
            cpf.append(11 - val if val > 1 else 0)

        return "%s%s%s.%s%s%s.%s%s%s-%s%s" % tuple(cpf)

    @staticmethod
    def gerar_aluno(serie_escolar="8º Ano"):
        """
        Gera um perfil completo de aluno.
        
        Args:
            serie_escolar (str): A série para calcular a idade aproximada.
        
        Returns:
            dict: Dicionário com dados do aluno.
        """
        # Lógica simples de idade baseada na série (aprox)
        # 1º ano ~ 6 anos, 8º ano ~ 13 anos
        idade_base = 6
        if "8" in serie_escolar:
            idade_base = 13
        elif "9" in serie_escolar:
            idade_base = 14
        
        # Data de nascimento baseada na idade
        ano_atual = date.today().year
        ano_nasc = ano_atual - idade_base
        nascimento = fake.date_of_birth(minimum_age=idade_base-1, maximum_age=idade_base+1)

        return {
            "nome_completo": fake.name(),
            "cpf": SchoolMockBR._gerar_cpf_valido(),
            "data_nascimento": nascimento.strftime("%d/%m/%Y"),
            "nome_mae": fake.name_female(),
            "matricula": str(random.randint(10000000, 99999999)),
            "situacao": random.choice(["Cursando", "Cursando", "Cursando", "Transferido"]),
            "serie_atual": serie_escolar
        }

    @staticmethod
    def gerar_escola():
        """Gera dados de uma escola fictícia."""
        estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        uf = random.choice(estados)
        
        return {
            "nome_escola": f"Escola Estadual {fake.last_name()} {fake.city_suffix()}",
            "codigo_inep": str(random.randint(11000000, 53999999)),
            "endereco": fake.street_address(),
            "cidade": fake.city(),
            "uf": uf,
            "rede": "Pública Estadual"
        }

    @staticmethod
    def gerar_turma_lote(qtd=10, serie="8º Ano"):
        """Gera uma lista de alunos para popular um banco de dados."""
        lista_alunos = []
        for _ in range(qtd):
            lista_alunos.append(SchoolMockBR.gerar_aluno(serie))
        return lista_alunos

# ==========================================
# BLOCO DE EXECUÇÃO E TESTE (SANITY CHECK)
# ==========================================
if __name__ == "__main__":
    print(">>> INICIANDO TESTE DO SCHOOLMOCK-BR <<<\n")
    
    # 1. Teste Aluno
    print("[1] Gerando Aluno (8º Ano):")
    aluno = SchoolMockBR.gerar_aluno("8º Ano")
    print(f"    Nome: {aluno['nome_completo']}")
    print(f"    CPF:  {aluno['cpf']}")
    print(f"    Nasc: {aluno['data_nascimento']}")
    
    # 2. Teste Escola
    print("\n[2] Gerando Escola:")
    escola = SchoolMockBR.gerar_escola()
    print(f"    Escola: {escola['nome_escola']}")
    print(f"    INEP:   {escola['codigo_inep']}")
    print(f"    Local:  {escola['cidade']} - {escola['uf']}")
    
    # 3. Teste Lote
    print("\n[3] Gerando Lote (5 Alunos):")
    turma = SchoolMockBR.gerar_turma_lote(5)
    for i, a in enumerate(turma):
        print(f"    {i+1}. {a['nome_completo']} ({a['situacao']})")
        
    print("\n>>> SUCESSO! CÓDIGO PRONTO PARA REGISTRO NO INPI. <<<")