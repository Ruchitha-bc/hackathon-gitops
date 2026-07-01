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

        // ADD THIS STAGE
        stage('Skip Jenkins Commit') {
            steps {
                script {
                    def author = sh(
                        script: 'git log -1 --pretty=%an',
                        returnStdout: true
                    ).trim()

                    if (author == "Jenkins") {
                        currentBuild.result = 'SUCCESS'
                        error("Skipping build because this commit was created by Jenkins.")
                    }
                }
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

        stage('Commit and Push GitOps Changes') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh '''
                    git config user.name "Jenkins"
                    git config user.email "jenkins@example.com"

                    git add apps/frontend/deployment.yaml
                    git add apps/backend/deployment.yaml

                    git diff --cached --quiet || git commit -m "Update image tags to build ${BUILD_NUMBER}"

                    git push https://${GIT_USER}:${GIT_TOKEN}@github.com/Ruchitha-bc/hackathon-gitops.git HEAD:main
                    '''
                }
            }
        }
    }
}
