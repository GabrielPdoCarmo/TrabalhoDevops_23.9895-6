pipeline {
    agent any

    stages {
        stage('Cloning repository') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/GabrielPdoCarmo/TrabalhoDevops_23.9895-6.git'
            }
        }

        stage('Build') {
            steps {
                script {
                    echo 'Stopping and removing existing containers...'
                    sh 'docker-compose down -v'

                    echo 'Building Docker images...'
                    sh 'docker-compose build'
                }
            }
        }

        stage('Start') {
            steps {
                script {
                    echo 'Starting Docker containers...'
                    sh 'docker-compose up -d'
                }
            }
        }
    }
}
