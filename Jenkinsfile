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
