environment {
  SONARSERVER = 'sonarserver'
  SONARSCANNER= 'sonarscanner'
}

node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool "${SONARSCANNER}";
    withSonarQubeEnv("${SONARSERVER}") {
      sh "${scannerHome}/bin/sonar-scanner"
    }
  }
}
