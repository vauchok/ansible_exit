node("${env.SLAVE}") {
  def maven_home = '/opt/apache-maven-3.5.2'
  def branch_name = 'master'

  stage('Preparation (Checking out)') {
    checkout scm: [$class: 'GitSCM', branches: [[name: "*/${branch_name}"]], userRemoteConfigs: [[url: 'https://github.com/vauchok/ansible_exit.git']]]
  }

  stage("Build"){
    /*
        Update file src/main/resources/build-info.txt with following details:
        - Build time
        - Build Machine Name
        - Build User Name
        - GIT URL: ${GIT_URL}
        - GIT Commit: ${GIT_COMMIT}
        - GIT Branch: ${GIT_BRANCH}

        Simple command to perform build is as follows:
        $ mvn clean package -DbuildNumber=$BUILD_NUMBER
    */
    sh "echo build artefact"
    sh "${maven_home}/bin/mvn clean package -DbuildNumber=$BUILD_NUMBER"
  }

  stage("Package"){
    /*
        usew tar tool to package built war file into *.tar.gz package
    */
    sh "echo package artefact"
  sh "cd target/ && tar -czvf ${BUILD_NUMBER}.tar.gz *.war"
  }

  stage("Roll out Dev VM"){
    /*
        use ansible to create VM (with developed vagrant module)
    */
    sh "echo ansible-playbook createvm.yml ..."
    sh "ansible-playbook createvm.yml -i localhost, -c local -vv"
  }

  stage("Provision VM"){
    /*
        use ansible to provision VM
        Tomcat and nginx should be installed
    */
    sh "echo ansible-playbook provisionvm.yml ..."
    sh "ansible-playbook provisionvm.yml -vv"
  }

  stage("Deploy Artefact"){
    /*
        use ansible to deploy artefact on VM (Tomcat)
        During the deployment you should create file: /var/lib/tomcat/webapps/deploy-info.txt
        Put following details into this file:
        - Deployment time
        - Deploy User
        - Deployment Job
    */
    sh "echo ansible-playbook deploy.yml -e artefact=... ..."
    sh "ansible-playbook deploy.yml -e 'artifact=mnt-exam.war job_name=$JOB_NAME url=exittask'"
  }

  stage("Test Artefact is deployed successfully"){
    /*
        use ansible to artefact on VM (Tomcat)
        During the deployment you should create file: /var/lib/tomcat/webapps/deploy-info.txt
        Put following details into this file:
        - Deployment time
        - Deploy User
        - Deployment Job
    */
    sh "echo ansible-playbook application_tests.yml -e artefact=... ..."
    sh "ansible-playbook application_tests.yml -e url=exittask"
  }

}

