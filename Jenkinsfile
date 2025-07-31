pipeline {
    agent any
    environment {
        DOCKER_HUB_USERNAME = 'tushar07051995'  // Replace with your Docker Hub username
        IMAGE_NAME = 'simple-flask-webapp'
        IMAGE_TAG = 'latest'
        REGISTRY = 'docker.io'  // Docker Hub registry
    }
    triggers {
        pollSCM('H/5 * * * *')  // Poll SCM every 5 minutes
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building the Docker image'
                sh 'docker build -t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing the Docker image'
                sh '''
                    docker run --rm -p 5001:5000 -d ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 10  # Allow time for app startup
                    CONTAINER_ID=$(docker ps -q --filter ancestor=${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG})
                    docker logs $CONTAINER_ID  # Debug logs
                    if [ -z "$CONTAINER_ID" ] || [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER_ID)" != "true" ]; then
                        echo "Container failed to run or exited"
                        exit 1
                    fi
                    curl -f http://localhost:5001/hello || { echo "Test failed"; exit 1; }
                    docker stop $CONTAINER_ID || true
                '''
            }
        }
        stage('Push') {
            steps {
                echo 'Pushing the Docker image to Docker Hub'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                        echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin ${REGISTRY}
                        docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }
    }
    post {
        always {
            sh 'docker logout ${REGISTRY} || true'
            archiveArtifacts artifacts: 'app.py', allowEmptyArchive: true
        }
        failure {
            echo 'Build failed due to script or file issues.'
        }
        success {
            echo 'Build completed successfully!'
        }
    }
}