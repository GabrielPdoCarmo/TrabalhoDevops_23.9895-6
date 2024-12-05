# Trabalho devops


### Aluno
- Gabriel Pereira do Carmo RA: 23.98.95-6

# Rodar Projeto

Para rodar o projeto, é necessário rodar o seguinte comando
```bash
docker-compose up --build
```
Caso venha ocorrer alguns erro, peço que rode novamente o comando acima

####  Inicio do projeto
O arquivo docker-compose.yml foi criado na raiz do projeto para configurar os contêineres necessários.

```bash
nano docker-compose.yml
```
Após isso adicionei o seguinte código dentro do arquivo:

``` yml
version: '3.7'

services:
  mariadb:
    build:
      context: ./mariadb
      dockerfile: Dockerfile_mariadb
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: school_db
      MYSQL_USER: flask_user
      MYSQL_PASSWORD: flask_password

  flask:
    build:
      context: ./flask
      dockerfile: Dockerfile_flask
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=mysql+pymysql://flask_user:flask_password@mariadb:3306/school_db
    depends_on:
      - mariadb

  test:
    build:
      context: ./flask
      dockerfile: Dockerfile_flask
    command: ["pytest", "/app/test_app.py"]  # Roda os testes no arquivo test_app.py
    depends_on:
      - mariadb
      - flask
    environment:
      - DATABASE_URL=mysql+pymysql://flask_user:flask_password@mariadb:3306/school_db
    networks:
      - default  # Conecta o contêiner aos mesmos serviços de rede
```

Após, criei uma pasta chamada `flask`, onde dentro crie o arquivo `app.py`.
```
nano app.py 
```
em seguinda, foi colocado o seguinte código:
``` python
# Código principal do Flask (app.py)
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from sqlalchemy.exc import OperationalError
from prometheus_flask_exporter import PrometheusMetrics
import logging

app = Flask(__name__)

metrics = PrometheusMetrics(app)
# Configuração da chave secreta para sessões
app.config['SECRET_KEY'] = 'minha_chave_secreta_super_secreta'  # Substitua por uma chave segura

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_password@mariadb/school_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o banco de dados e o AppBuilder
db = SQLAlchemy(app)
appbuilder = AppBuilder(app, db.session)

# Configuração do log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelo de Aluno - Definição da tabela 'Aluno' no banco de dados
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    disciplinas = db.Column(db.String(200), nullable=False)
    ra = db.Column(db.String(200), nullable=False)


# Tentar conectar até o MariaDB estar pronto
attempts = 5
for i in range(attempts):
    try:
        with app.app_context():
            db.create_all()  # Inicializa o banco de dados
            # Criar um usuário administrador padrão
            if not appbuilder.sm.find_user(username='admin'):
                appbuilder.sm.add_user(
                    username='admin',
                    first_name='Admin',
                    last_name='User',
                    email='admin@admin.com',
                    role=appbuilder.sm.find_role(appbuilder.sm.auth_role_admin),
                    password='admin'
                )
        logger.info("Banco de dados inicializado com sucesso.")
        break
    except OperationalError:
        if i < attempts - 1:
            logger.warning("Tentativa de conexão com o banco de dados falhou. Tentando novamente em 5 segundos...")
            time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente
        else:
            logger.error("Não foi possível conectar ao banco de dados após várias tentativas.")
            raise

# Visão do modelo Aluno para o painel administrativo
class AlunoModelView(ModelView):
    datamodel = SQLAInterface(Aluno)
    list_columns = ['id', 'nome', 'sobrenome', 'turma', 'disciplinas', 'ra']

# Adicionar a visão do modelo ao AppBuilder
appbuilder.add_view(
    AlunoModelView,
    "Lista de Alunos",
    icon="fa-folder-open-o",
    category="Alunos",
)

# Rota para listar todos os alunos - Método GET
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    output = [{'id': aluno.id, 'nome': aluno.nome, 'sobrenome': aluno.sobrenome, 'turma': aluno.turma, 'disciplinas': aluno.disciplinas, 'ra': aluno.ra} for aluno in alunos]
    return jsonify(output)

# Rota para adicionar um aluno - Método POST
@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    novo_aluno = Aluno(nome=data['nome'], sobrenome=data['sobrenome'], turma=data['turma'], disciplinas=data['disciplinas'], ra=data['ra'])
    db.session.add(novo_aluno)
    db.session.commit()
    logger.info(f"Aluno {data['nome']} {data['sobrenome']} adicionado com sucesso!")
    return jsonify({'message': 'Aluno adicionado com sucesso!'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

Após adicionei as dependencias da aplicação por meio do arquivo `requirements`, que ficou dentro da pasta `flask` também.

```bash
nano requirements.txt
```

e adicionei o seguinte código dentro:
```txt
Flask==1.1.4  # Versão compatível com Flask-AppBuilder
Flask-SQLAlchemy==2.4.4  # Extensão do Flask para integração com SQLAlchemy
PyMySQL==0.9.3  # Biblioteca para conexão do Python com o banco de dados MariaDB
Flask-AppBuilder==3.3.0  # Versão compatível com Flask 1.x
Werkzeug==1.0.1  # Versão compatível do Werkzeug para evitar erros de importação
MarkupSafe==2.0.1  # Versão compatível com Jinja2 e Flask
WTForms==2.3.3  # Versão compatível com Flask-AppBuilder que contém o módulo 'compat'
prometheus-flask-exporter==0.18.3
pytest==6.2.5
pytest-flask==1.2.0
Flask-Testing==0.8.0
```
Após criei o `Dockerfile_flask` dentro da pasta `flask` também, onde ele vai determinar o diretorio de trabalho e rodar a instalação das dependencias

``` bash
vim Dockerfile_flask
```

e em seguida o seguinte código foi adicionado dentro:

``` yml
# Dockerfile (Flask AppBuilder)
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .
COPY app.py /app/

CMD ["flask", "run", "--host=0.0.0.0"]

```

Em seguida, na raiz do projeto, criei a pasta `mariadb` e adicionei o arquivo `Dockerfile_mariadb`, responsável por definir as variáveis de ambiente necessárias para o funcionamento do projeto.

```nano
nano Dockerfile_mariadb
```

Foi colocado o seguinte código: 

```  yml
# Dockerfile para MariaDB
# Salve este arquivo como Dockerfile.mariadb na raiz do projeto

# Dockerfile (MariaDB)
FROM mariadb:10.5

# Defina as variáveis de ambiente para o banco de dados
ENV MYSQL_ROOT_PASSWORD=root_password
ENV MYSQL_DATABASE=school_db
ENV MYSQL_USER=flask_user
ENV MYSQL_PASSWORD=flask_password

EXPOSE 3306
```



- Ao confeir no navegador o localhost:5000 obitive a resultado correto:

![alt text](imagens/FAB.png)

#### Configuração do Jenkins
Nesta etapa, eu criei uma nova tarefa no Jenkins, que será utilizada para gerenciar o pipeline do projeto "trabalho devOps". Primeiro, defini o nome do item como "trabalho devOps". Em seguida, escolhi o tipo de tarefa como "Pipeline", pois é o mais indicado para projetos que exigem a execução de processos complexos e sequenciais, como o fluxo de integração e entrega contínua (CI/CD). Depois de selecionar o tipo de tarefa, cliquei no botão "Confirmar" para prosseguir com a configuração do pipeline.

![alt text](imagens/Jenkins_1.png)

Em seguida, configurei o pipeline no Jenkins para conectar ao repositório Git onde está armazenado o código do projeto "Trabalho DevOps".

No campo SCM, selecionei Git como o sistema de controle de versão.  
No campo Repository URL, inseri o link para o repositório do GitHub: https://github.com/GabrielPdoCarmo/TrabalhoDevops_23.9895-6.git.  
Como não foram configuradas credenciais específicas, deixei o campo Credentials como - none -. Caso o repositório fosse privado, seria necessário adicionar credenciais para autenticação.  

No campo Branches to build, especifiquei a branch que seria usada para as builds, no caso */master. Isso indica que o pipeline será executado na branch principal.

![alt text](imagens/Jenkins_2.png)

### Desenvolvimento do Grafana e Prometheus
Adicionada as pastas grafana e prometheus aos arquivos.
Na pasta `grafana` o arquivo `Dockerfile_grafana` fica responsável por crir a imagem Docker personalizada para o serviço Grafana. Ela define como configurar o ambiente, adicionando configurações específicas, plugins e integrações necessárias para funcionar no contexto da aplicação.
Código:
```  yml
FROM grafana/grafana:latest

USER root

RUN mkdir /var/lib/grafana/dashboards

COPY provisioning/datasource.yml /etc/grafana/provisioning/datasources/
COPY provisioning/dashboard.yml /etc/grafana/provisioning/dashboards/
COPY dashboards/mariadb_dashboard.json /var/lib/grafana/dashboards/

RUN chown -R 472:472 /etc/grafana/provisioning

USER grafana
```
Na pasta `dashboards` do Grafana, temos o arquivo responsável por um dashboard pré-configurado, que contém a definição de painéis e métricas específicas para monitorar um banco de dados MariaDB. Ele define os painéis, as métricas monitoradas e a integração com os datasources.
Arquivo:
`mariadb_dashboard.json`

````
 {
  "uid": "simple_dashboard",
  "title": "Desempenho HTTP - Métricas Padrão",
  "tags": ["HTTP", "Prometheus", "Desempenho"],
  "timezone": "browser",
  "schemaVersion": 16,
  "version": 1,
  "panels": [
    {
      "type": "graph",
      "title": "Taxa de Requisições HTTP",
      "datasource": "Prometheus",
      "gridPos": { "x": 0, "y": 0, "w": 12, "h": 6 },
      "targets": [
        {
          "expr": "rate(prometheus_http_requests_total[1m])",
          "legendFormat": "Requisições/s",
          "refId": "A"
        }
      ],
      "lines": true,
      "linewidth": 2,
      "fill": 1
    },
    {
      "type": "graph",
      "title": "Latência Média de Requisições",
      "datasource": "Prometheus",
      "gridPos": { "x": 12, "y": 0, "w": 12, "h": 6 },
      "targets": [
        {
          "expr": "rate(prometheus_http_request_duration_seconds_sum[1m]) / rate(prometheus_http_request_duration_seconds_count[1m])",
          "legendFormat": "Latência Média (s)",
          "refId": "B"
        }
      ],
      "lines": true,
      "linewidth": 2,
      "fill": 1
    },
    {
      "type": "graph",
      "title": "Requisições HTTP em Andamento",
      "datasource": "Prometheus",
      "gridPos": { "x": 0, "y": 6, "w": 12, "h": 6 },
      "targets": [
        {
          "expr": "promhttp_metric_handler_requests_in_flight",
          "legendFormat": "Em andamento",
          "refId": "C"
        }
      ],
      "lines": true,
      "linewidth": 2,
      "fill": 1
    },
    {
      "type": "graph",
      "title": "Requisições HTTP - Taxa de Erro",
      "datasource": "Prometheus",
      "gridPos": { "x": 12, "y": 6, "w": 12, "h": 6 },
      "targets": [
        {
          "expr": "rate(prometheus_http_requests_total{status!~'2..'}[1m])",
          "legendFormat": "Taxa de Erro",
          "refId": "D"
        }
      ],
      "lines": true,
      "linewidth": 2,
      "fill": 1
    }
  ],
  "refresh": "10s",
  "time": { "from": "now-1h", "to": "now" },
  "overwrite": true
}
````

Na outra pasta, provisioning temos dois arquivos. `datasource.yml` e `dashboard.yml` que são responsáveis por automatizar a configuração de dashboards e fontes de dados. Eles permitem que você configure essas opções automaticamente durante a inicialização do Grafana, em vez de configurá-las manualmente pela interface do usuário.
`datasource.yml`É aquele que contém arquivos YML para configurar datasources (fontes de dados), como Prometheus, MySQL, Elasticsearch, entre outros.
````
apiVersion: 1  # Versão da API utilizada para configuração do Grafana

datasources:
  - name: Prometheus  # Nome da fonte de dados que será adicionada no Grafana
    type: prometheus  # Tipo da fonte de dados, neste caso, Prometheus
    access: proxy  # Tipo de acesso, 'proxy' significa que as requisições passarão pelo backend do Grafana
    url: http://prometheus:9090  # URL para acessar o Prometheus dentro da rede do Docker
    isDefault: true  # Define esta fonte de dados como a padrão no Grafana
    jsonData:
      timeInterval: 5s  # Intervalo de tempo padrão para coleta de dados

````

`dashboards.yml` É aquele que contém arquivos YML para provisionar dashboards, especificando onde estão os arquivos JSON com as definições dos dashboards.

````
apiVersion: 1

providers:
  - name: "MariaDB Dashboards"
    orgId: 1
    folder: ""
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /var/lib/grafana/dashboards
````
Na pasta `prometheus`, temos o arquivo `prometheus.yml`, que contém a configuração principal do Prometheus. Nesse arquivo, são definidas as configurações para:

1. **Fontes de coleta de métricas (alvos)**: Especificação das fontes de dados que o Prometheus deve monitorar.
2. **Regras de scrape**: Definição da frequência e comportamento da coleta das métricas.
3. **Alertas (Alertmanager)**: Configurações para o gerenciamento de alertas, incluindo a integração com o Alertmanager.
4. **Configurações de armazenamento**: Parâmetros relacionados ao armazenamento de dados e outras configurações globais do Prometheus.

Essas configurações permitem ajustar como o Prometheus coleta, armazena e gerencia as métricas e alertas em seu ambiente.
````
global:
  scrape_interval: 15s  # Coleta de métricas a cada 15 segundos para todos os jobs

scrape_configs:
  - job_name: 'prometheus'  # Coleta de métricas do Prometheus
    static_configs:
      - targets: 
          - 'localhost:9090'  # Alvo é o próprio Prometheus

  - job_name: 'mysqld_exporter'  # Coleta de métricas do MySQL
    static_configs:
      - targets: 
          - '192.168.100.8:9104'  # Alvo é o MySQL Exporter

````

Outras alterações se fizeram necessárias ao adicionar essas configurações. Alterações no docker-compose e Jenkinsfile.
`docker-compose.yml`
``` yml
services:
  flask:
    build:
      context: ./flask
      dockerfile: Dockerfile_flask
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
    depends_on:
      - mariadb

  mariadb:
    build:
      context: ./mariadb
      dockerfile: Dockerfile_mariadb
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: school_db
      MYSQL_USER: flask_user
      MYSQL_PASSWORD: flask_password

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    depends_on:
      - mysqld_exporter
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"

  mysqld_exporter:
    image: prom/mysqld-exporter
    ports:
      - "9104:9104"
    environment:
      DATA_SOURCE_NAME: "user:password@(mariadb:3306)/"
    depends_on:
      - mariadb

  grafana:
    build:
      context: ./grafana
      dockerfile: Dockerfile_grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

  test:
    build:
      context: ./flask
      dockerfile: Dockerfile_flask
    command: ["pytest", "/app/test_app.py"]  # Roda os testes no arquivo test_app.py
    depends_on:
      - mariadb
      - flask
    environment:
      - DATABASE_URL=mysql+pymysql://flask_user:flask_password@mariadb:3306/school_db
    networks:
      - default 
```

Jenkinsfile
``` yml
pipeline {
    agent any

    environment {
        CONTAINER_SERVICES = 'mariadb flask test mysqld_exporter prometheus grafana'
    }

    stages {
        stage('Git Pull & Build Containers') {
            steps {
                script {
                    git branch: "master", url: "https://github.com/GabrielPdoCarmo/TrabalhoDevops_23.9895-6.git"
                    sh 'docker-compose down -v'
                    sh 'docker-compose build'
                }
            }
        }

        stage('Initialize and Start Containers') {
            steps {
                script {
                    sh "docker-compose up -d ${env.CONTAINER_SERVICES}"
                    sh 'sleep 40'  
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        sh 'docker-compose run --rm test'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error "Testes falharam. Pipeline interrompido."
                    }
                }
            }
        }

        stage('Keep Application Running') {
            steps {
                script {
                    sh 'docker-compose up -d'
                }
            }
        }
    }

    post {
        failure {
            sh 'docker-compose down -v'
        }
    }
}
```

Após isso tivemos o dashboard funcionando de forma automatizada a partir de métricas do prometheus.
![image](imagens/Grafana.PNG)


