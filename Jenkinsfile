node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    withSonarQubeEnv() {
      sh "/home/catB/wg275589/software/sonar-scanner-4.8.0.2856-linux/bin/sonar-scanner"
    }
  }
}
