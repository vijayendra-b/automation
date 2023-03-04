pipeline {
    agent any
    environment {
            DOCKERHUB_CREDENTIALS = credentials('myDockerHub')
    }
    stages {
        stage('Build Image') {
            steps {

                sh "docker build -t='vijayendra1/testscripts:jenkins' . "

            }
        }
        stage('Login to Docker Hub') {
          steps {
            sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
          }
        }
        stage('Push Image') {
            steps {
			        sh "docker push vijayendra1/testscripts:jenkins"
            }
        }
    }
    post {
        always {
          sh 'docker logout'
        }
    }
}