node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scannerHome = tool "sonarscanner";
    withSonarQubeEnv("sonarserver") {
      sh "${scannerHome}/sonar-scanner-cli-4.8.0.2856-linux/bin/sonar-scanner"
    }
  }
}
