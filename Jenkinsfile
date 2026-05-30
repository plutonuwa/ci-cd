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

        stage('Unit Tests') {
            steps {
                bat 'npm test'       // no need for chmod on Windows
            }
        }

        stage('Linting') {
            steps {
                // cmd /c makes || true equivalent work on Windows
                bat 'npx eslint src/ --ext .js || exit /b 0'
            }
        }

        stage('E2E Tests') {
            steps {
                bat 'npx playwright install --with-deps chromium'

                // Start server in background on Windows using START
                bat '''
                    START /B npm start
                    timeout /t 3 /nobreak
                    npx playwright test
                '''
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