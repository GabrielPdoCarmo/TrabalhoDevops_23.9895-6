pipeline {
    agent any

<<<<<<< HEAD
    stages {
        stage('Clonar Repositório') {	
            steps {
                git branch: 'master', url: 'https://github.com/GabrielPdoCarmo/TrabalhoDevops_23.9895-6.git'
=======
    environment {
        GIT_REPO = 'https://github.com/GabrielPdoCarmo/TrabalhoDevops_23.9895-6.git'
        GIT_BRANCH = 'master'
    }

    stages {
        stage('Baixar o Código do Repositório') {
            steps {
                script {
                    // Clonando o repositório Git
                    git url: "${GIT_REPO}", branch: "${GIT_BRANCH}"
                }
>>>>>>> 51fe482c7a4dd64ea235a98e792b4a392ffc95a9
            }
        }

        stage('Construção e Inicialização') {
            steps {
                sh 'docker-compose up -d mariadb flask test mysqld_exporter prometheus grafana'
            }
        }

        stage('Build da Aplicação') {
            steps {
                  sh 'docker-compose down -v || true' // Ignorar erros se os contêineres não estiverem ativos
                    sh 'docker-compose build'

            }
        }

        stage('Criar Imagens Docker') {
            steps {
                script {
<<<<<<< HEAD
                    def appImage = docker.build('seu-usuario/seu-app')
                    appImage.push("latest")
=======
                    // Criando as imagens Docker para os serviços definidos
                    sh 'docker-compose build'

                    // Inicializando os containers em segundo plano
                    sh 'docker-compose up -d'
                }
            }
        }

        stage('Execução dos Testes') {
            steps {
                script {
                    // Aguardando os containers estarem prontos
                    sh 'sleep 40'
                    
                    // Rodando os testes no container 'test'
                    sh 'docker-compose run --rm test'
>>>>>>> 51fe482c7a4dd64ea235a98e792b4a392ffc95a9
                }
            }
        }

<<<<<<< HEAD
        stage('Deploy e Subir Ambiente') {
            steps {
                sh 'docker-compose down && docker-compose up -d'
            }
        }

        stage('Monitorar Ambiente') {
            steps {
                sh 'curl http://localhost:8080/health' // Exemplo de verificação de status
            }
=======
    post {
        success {
            echo 'A pipeline foi executada com sucesso!'
        }
        failure {
            echo 'A execução da pipeline falhou.'
>>>>>>> 51fe482c7a4dd64ea235a98e792b4a392ffc95a9
        }
    }
}
