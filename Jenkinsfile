node {
  stage('SCM')
  {
    checkout scm
  }
  stage('External Analizer')
  {
    //Put your command line for your external analyzer
    //Dont forget to precise you want your command to run on a terminal
  }
  stage('SonarQube Analysis') 
  {
    def scannerHome = tool "sonarscanner";
    withSonarQubeEnv("sonarserver")
    {
      sh "${scannerHome}/bin/sonar-scanner"
    }
  }
}
