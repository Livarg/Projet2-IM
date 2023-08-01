node {
  stage('SCM') {
    checkout scm
  }
  stage('SonarQube Analysis') {
    withSonarQubeEnv("sonarserver") {
      sh '''SONAR=$(which sonar-scanner)
            eval $SONAR'''
    }
  }
}
