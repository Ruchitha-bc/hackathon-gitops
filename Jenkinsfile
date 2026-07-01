pipeline {
    agent any

    environment {
        FRONTEND_IMAGE = "diyacmenezes202/frontend"
        BACKEND_IMAGE = "diyacmenezes202/backend"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Frontend') {
            steps {
                sh 'docker build -t $FRONTEND_IMAGE:${BUILD_NUMBER} ./apps/frontend'
            }
        }

        stage('Build Backend') {
            steps {
                sh 'docker build -t $BACKEND_IMAGE:${BUILD_NUMBER} ./apps/backend'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                }
            }
        }

        stage('Push Images') {
            steps {
                sh 'docker push $FRONTEND_IMAGE:${BUILD_NUMBER}'
                sh 'docker push $BACKEND_IMAGE:${BUILD_NUMBER}'
            }
        }

        stage('Update Deployment YAML') {
            steps {
                sh '''
                sed -i "s|image: .*frontend:.*|image: ${FRONTEND_IMAGE}:${BUILD_NUMBER}|g" apps/frontend/deployment.yaml
                sed -i "s|image: .*backend:.*|image: ${BACKEND_IMAGE}:${BUILD_NUMBER}|g" apps/backend/deployment.yaml
                '''
            }
        }

    }
}
