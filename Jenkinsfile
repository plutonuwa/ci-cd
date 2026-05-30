pipeline {
    agent any

    tools {
        // This ensures Node.js is installed. 
        // Note: 'node20' must match the name configured in your Jenkins Global Tool Configuration.
        nodejs 'node20' 
    }

    stages {
        stage('Checkout') {
            steps {
                // Pulls the code from your Git repository
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Equivalent to 'npm ci'
                sh 'npm ci'
            }
        }

        stage('Unit Tests') {
            steps {
                // Equivalent to your 'test' job steps
                sh 'chmod +x node_modules/.bin/jest'
                sh 'npm test'
            }
        }

        stage('Linting') {
            steps {
                // The '|| true' ensures the pipeline doesn't fail if linting fails, just like GitHub Actions
                sh 'npx eslint src/ --ext .js || true'
            }
        }

        stage('E2E Tests') {
            steps {
                // Jenkins stages run sequentially by default, so this naturally acts like 'needs: test'
                sh 'npx playwright install --with-deps chromium'
                
                // Running the server in the background and waiting for it to boot
                sh '''
                    npm start &
                    sleep 3
                    npx playwright test
                '''
            }
        }
    }

    post {
        always {
            // Clean up any background node processes left running from the E2E stage
            sh 'pkill -f "node" || true'
        }
    }
}