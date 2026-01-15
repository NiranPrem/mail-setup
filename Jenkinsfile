pipeline {
    agent any

    environment {
        SMTP_HOST = "smtp.gmail.com"
        SMTP_PORT = "465"
        SMTP_USE_SSL = "true"

        SMTP_USER = "niranprempanakal@gmail.com"
        SMTP_PASS = "kqlp ibua ckrf dipj"

        PYTHONUNBUFFERED = "1"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Files') {
            steps {
                sh '''
                  echo "Listing workspace files:"
                  ls -lh

                  test -f bulk_mailer.py
                  test -f recipients.txt
                  test -f Niran_Dev.pdf
                '''
            }
        }

        stage('Send Emails') {
            steps {
                sh '''
                  echo "Running bulk mailer..."
                  python3 bulk_mailer.py recipients.txt Niran_Dev.pdf
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Bulk email test completed successfully"
        }
        failure {
            echo "❌ Bulk email test failed"
        }
    }
}
