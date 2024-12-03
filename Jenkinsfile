pipeline {
    agent any

    stages {
        stage('Clonar Repositório') {	
            steps {
                git branch: 'master', url: 'https://github.com/GabrielPdoCarmo/TrabalhoDevops_23.9895-6.git'
            }
        }

        stage('Rodar Testes') {
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
                    def appImage = docker.build('seu-usuario/seu-app')
                    appImage.push("latest")
                }
            }
        }

        stage('Deploy e Subir Ambiente') {
            steps {
                sh 'docker-compose down && docker-compose up -d'
            }
        }

        stage('Monitorar Ambiente') {
            steps {
                sh 'curl http://localhost:8080/health' // Exemplo de verificação de status
            }
        }
    }
}
