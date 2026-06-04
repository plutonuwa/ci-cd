pipeline {
    agent any

    tools {
        nodejs 'node20'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'npm ci'         // bat = Windows CMD, replaces sh
            }
        }

        stage('API tests'){
            steps{
                bat 'py -m venv .venv'
                // CRITICAL: We call the executable directly from the venv folder 
                // because separate 'bat' sessions don't persist environment activations.
                bat '.venv\\Scripts\\pip install -r ./backend/requirements.txt'
                bat '.venv\\Scripts\\pytest ./backend/test.py'
            }
        }
    }

    post {
        always {
            // Kill node processes on Windows
            bat 'taskkill /F /IM node.exe /T || exit /b 0'
        }
    }
}