pipeline {
    agent any

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

        stage('Start Containers & Run Tests') {
            steps {
                script {
                    sh 'docker-compose up -d mariadb flask test mysqld_exporter prometheus grafana'
                    sh 'sleep 40' 

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
                    sh 'docker-compose up -d mariadb flask test mysqld_exporter prometheus grafana'
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
