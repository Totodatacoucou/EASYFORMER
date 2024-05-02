pipeline {
    agent any
    environment {
        CREDENTIALS_FILE = '/home/vagrant/projet_Easyformer/credentials.json'
        DESTINATION_FOLDER = '/home/vagrant/projet_Easyformer/dossier_destination'
        SCRIPT_NAME = 'script.py'
    }
    stages {
        stage('Récupération du projet') {
            steps {
                git branch: 'main',
                credentialsId: 'JenkinsGitlabSSH',
                url: 'git@gitlab.easy.com:EsyFormer/test_easy.git'
            }
        }
        stage('Exécution du script Python') {
            steps {
                script {
                    // Copier le script Python dans le répertoire de travail du pipeline
                    sh "cp /home/vagrant/projet_Easyformer/${SCRIPT_NAME} ."
                    // Vérifier si le fichier credentials.json existe
                    if (!fileExists(CREDENTIALS_FILE)) {
                        error "Le fichier ${CREDENTIALS_FILE} n'existe pas."
                    }
                    // Exécuter le script Python
                    sh "python ${SCRIPT_NAME} ${CREDENTIALS_FILE} ${DESTINATION_FOLDER}"
                }
            }
        }
    }
}

def fileExists(filePath) {
    return file(filePath).exists()
}