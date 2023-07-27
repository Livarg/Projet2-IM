node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    def SonarHome= sh"$(which sonnar-scanner)"
    withSonarQubeEnv() {
      sh "${SonarHome}"
    }
  }
}
