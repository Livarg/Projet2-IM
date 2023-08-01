node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def scanner = sh 'which sonar-scanner';
    withSonarQubeEnv("sonarserver") {
      sh "${scanner}"
    }
  }
}
