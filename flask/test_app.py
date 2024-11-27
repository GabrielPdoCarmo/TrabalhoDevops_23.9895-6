import pytest
from flask import Flask
from flask.testing import FlaskClient

# Importar a aplicação Flask
from app import app, db, Aluno  # Assumindo que seu arquivo principal é app.py

@pytest.fixture
def client():
    # Configuração do client de teste Flask
    with app.test_client() as client:
        # Limpa o banco de dados antes de cada teste
        db.create_all()
        yield client
        # Limpa após o teste
        db.session.remove()
        db.drop_all()

def test_listar_alunos(client: FlaskClient):
    """Testa a rota GET /alunos"""
    # Adiciona um aluno para garantir que a lista não esteja vazia
    aluno = Aluno(nome="Gabriel", sobrenome="Carmo", turma="9B", disciplinas="Matemática, Física", ra="12345")
    db.session.add(aluno)
    db.session.commit()
    
    response = client.get('/alunos')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)  # Correção aqui: use get_json()
    assert len(response.get_json()) > 0  # Verifica se existe pelo menos um aluno

def test_adicionar_aluno(client: FlaskClient):
    """Testa a rota POST /alunos"""
    new_aluno = {
        "nome": "Gabriel",
        "sobrenome": "Carmo",
        "turma": "9B",
        "disciplinas": "Matemática, Física",
        "ra": "12345"
    }
    
    response = client.post('/alunos', json=new_aluno)
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Aluno adicionado com sucesso!'  # Correção aqui: use get_json()

    # Verifica se o aluno foi realmente adicionado ao banco de dados
    aluno = Aluno.query.filter_by(ra='12345').first()
    assert aluno is not None  # Verifica que o aluno foi adicionado
    assert aluno.nome == "Gabriel"
    assert aluno.sobrenome == "Carmo"
