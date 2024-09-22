# zenlegacy-GenAI

##Overview
Nanagara is a revolutionary tool designed to automate the generation of Docker, Docker Compose, and Kubernetes files for various frameworks, drastically reducing the time and effort required for manual configuration. Deploying applications has never been easier, especially for developers who often struggle to create accurate and efficient Docker and Kubernetes scripts.

With Nanagara, we provide:

AI-powered accurate script generation using LangChain, simplifying the setup for Flask backends and MySQL databases.
GitHub URL deployment, where users can directly deploy working projects from GitHub. Nanagara automatically builds Docker images, runs Docker Compose files, and sets up the application for deployment.
By simply inputting your environment variables, you can skip the hassle of script writing and focus on building your project. The generated scripts are accurate, tested, and ready for deployment, significantly simplifying the process for any developer or team.

##Features
1. AI-Powered Script Generation
Nanagara uses LangChain to provide automated Docker, Docker Compose, and Kubernetes scripts that are pre-tested and functional. The only thing you need to do is replace placeholder environment variables with your own, and the scripts will work perfectly.

Tested Technologies: Flask backend, MySQL database
Future Scalability: We are continuously expanding to support other frameworks, databases, and deployment configurations.
2. GitHub URL Deployment
Nanagara allows you to deploy any working GitHub repository in seconds. Simply input your GitHub link, and Nanagara will:

Build the Docker image
Run Docker Compose or Kubernetes files
Set up and launch the application on a local server
This tool automatically handles tasks like building Docker images, running the build file, and launching the application locally. You can view and interact with your deployed app seamlessly.


Using the Streamlit App
Prerequisites
Add the Groq API key to the .env file to enable the AI-powered script generation feature.

Navigate to the main directory of the project.

Run the following command to launch the Streamlit app:

streamlit run main.py   Features of the Streamlit App
Chat Mode: Powered by Groqchat using the Llama model, providing interactive chat functionalities. This mode is used for user requests and generates responses for accurate Docker and Kubernetes files.
Script Generation: For now, the system supports generating scripts for Flask backends with MySQL databases. Users can input details in a prompt, and the app generates highly accurate deployment files, which can be expanded to other frameworks with minimal effort.

##Future Improvements
We are continuously improving Nanagara to provide additional services, including:

Automatic requirements.txt generation: Automating the creation of Python requirements.txt files for any project.
Automated GitHub Actions workflows: Generating and pushing GitHub Action workflows for seamless CI/CD pipeline integration.
GitHub Repository Interaction: Nanagara will offer a chat feature that interacts with GitHub repositories. Users will be able to:
Chat with their repositories
Generate CI/CD workflows
Fetch file structures, and even push deployment files directly to GitHub.
Document Parsing: Users will be able to provide application descriptions from PDFs or Word documents, and Nanagara will automatically generate the project’s file structure and required deployment files based on this information.
Kubernetes Note
While Nanagara generates Kubernetes files, these have not been fully tested yet. We are actively working on finding the most accurate way to test and ensure they work smoothly in production environments.

##Conclusion
Nanagara provides a dual service that significantly helps with deployment:

Accurate, AI-powered generation of Docker, Docker Compose, and Kubernetes files, customized for specific environments and frameworks.
Instant deployment from GitHub URLs, streamlining the process of building and launching your applications locally.
We are focused on making deployment faster and easier, automating the most time-consuming parts of the process, and improving as we go. Whether you need custom deployment files or instant GitHub deployment, Nanagara has you covered.
 
### Setup Guide

This Project contains following services and folders:

- `api-server`: HTTP API Server for REST API's
- `build-server`: Docker Image code which clones, builds and pushes the build to S3
- `s3-reverse-proxy`: Reverse Proxy the subdomains and domains to s3 bucket static assets

### Local Setup

1. Run `npm install` in all the 3 services i.e. `api-server`, `build-server` and `s3-reverse-proxy`
2. Docker build the `build-server` and push the image to AWS ECR.
3. Setup the `api-server` by providing all the required config such as TASK ARN and CLUSTER arn.
4. Run `node index.js` in `api-server` and `s3-reverse-proxy`

At this point following services would be up and running:

| S.No | Service            | PORT    |
| ---- | ------------------ | ------- |
| 1    | `api-server`       | `:9000` |
| 2    | `socket.io-server` | `:9002` |
| 3    | `s3-reverse-proxy` | `:8000` |


