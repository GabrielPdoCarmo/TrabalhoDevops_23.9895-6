pipeline {
    agent any

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
            }
        }

        stage('Construção e Inicialização') {
            steps {
                script {
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
                }
            }
        }
    }

    post {
        success {
            echo 'A pipeline foi executada com sucesso!'
        }
        failure {
            echo 'A execução da pipeline falhou.'
        }
    }
}
