podTemplate(
  serviceAccount: 'jenkins-admin',
  containers: [
    containerTemplate(
      name: 'jnlp',
      image: 'msd117/jenkins-generic-agent:1.1.2-bookworm-jdk21',
      ttyEnabled: true
    )
  ],
  namespace: 'devops-tools'
) {
  node(POD_LABEL) {
    stage('Clone') {
      container('jnlp') {
        git branch: 'main',
          credentialsId: 'github-home-kops-token',
          url: 'https://github.com/home-kops/slskd-docker.git'
      }
    }

    stage('Verify') {
      container('jnlp') {
        sh 'echo "Verifying the environment..."'
      }
    }
  }
}
