node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool "sonarscanner";
    withSonarQubeEnv("sonarserver") {
      sh "${scannerHome}/bin/sonar-scanner"
    }
  }
}
