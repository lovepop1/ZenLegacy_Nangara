import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

def app():
    # Load environment variables
    load_dotenv()

    # Initialize the Groq client
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    # Set custom CSS for better visuals
    st.markdown("""
        <style>
        body {
            background-color: #F0F2F6;
        }
        h1 {
            color: #005BFF;
        }
        h2 {
            color: #FF9900;
        }
        .stButton>button {
            background-color: #FF4B4B;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    # Title of the app
    st.title("AI-Powered Deployment Script Generator")
    st.subheader("Generate deployment scripts for Flask applications effortlessly!")

    # Input section: Project Details
    st.header("1. Project Details")
    project_name = st.text_input("Project Name", key="project_name")
    app_description = st.text_area("Describe your Flask application:", height=150, key="app_description")
    entry_point = st.text_input("Entry Point (e.g., manage.py)", value="app.py", key="entry_point")
    ports = st.text_input("Ports (e.g., 8000)", value="8000", key="ports")

    # Input section: Dependencies and Environment
    st.header("2. Dependencies and Environment")
    dependencies = st.file_uploader("Upload Dependencies File (requirements.txt)", key="dependencies")
    env_vars = st.text_area("Environment Variables:", height=100, key="env_vars", value="Format:\nDATABASE_URL=mysql://user:password@hostname:port/dbname\nSECRET_KEY=your_secret_key\nDEBUG=False\nALLOWED_HOSTS=yourdomain.com\n\nEnter other environment variables here")
    caching_service = st.selectbox("Select Caching Service:", ["Redis", "Memcached", "None"], key="caching_service")
    
    python_version = st.text_input("Python version", key="python_version", value="python 3.12")
    sql_version = st.text_input("MySQL Version (e.g., 8.0)", key="sql_version", value="8.0")

    # Input section: Deployment Specific
    st.header("3. Deployment Specific")
    environment = st.selectbox("Environment Type:", ["Local", "Development", "Staging", "Production"], key="environment")
    container_orchestration = st.selectbox("Container Orchestration:", ["Docker", "Docker and Kubernetes"], key="container_orchestration")

    # Show Kubernetes-specific fields only when "Docker and Kubernetes" is selected
    if container_orchestration == "Docker and Kubernetes":
        auto_scaling = st.checkbox("Enable Auto-Scaling", key="auto_scaling")
        persistence = st.text_area("Volume Mounts (e.g., /data:/var/data):", height=100, key="persistence")
        load_balancer = st.checkbox("Enable Load Balancer", key="load_balancer")
        health_check = st.text_input("Health Check Route (e.g., /health)", key="health_check")


    # Button to generate deployment scripts
    if st.button("Generate Deployment Scripts"):
        docker_output = None
        docker_compose_output = None
        k8s_output = None

        # Docker prompt text for Dockerfile
        
        docker_prompt_text = (
        "Generate a Dockerfile for a Flask application with the following details:\n"
        "Do not give any introduction, conclusion or extra text, just the exact accurate code.Focus only on Flask docker, mysql can be done later. use use the below versions to create the docker. do not run seperate command t install django , everything is there in requirements.txt"
        "The Dockerfile should be accurate and work properly.\n"
        f"Project Name: {project_name}\n"
        f"Description: {app_description}\n"
        f"Entry point: {entry_point}\n"
        f"Dependencies: {dependencies}\n"
        f"Caching Service: {caching_service}\n"
        f"Python Version: {python_version}\n"
        f"Ports: {ports}\n"
        "Do not include any explanations in the code.No introduction or extra texts , just give the accurate code"
        )

    # Docker Compose prompt text (with SQL version)
        docker_compose_prompt_text = (
        "Generate a Docker Compose file for the same Flask application and MySQL, "
        "configuring services for the database, caching service, and Flask. "
        "No introduction, conclusion, or any extra text or paragraphs, just directly give the code.\n"
        f"Description: {app_description}\n"
        f"Entry point: {entry_point}\n"
        f"Dependencies: {dependencies}\n"
        f"Caching Service: {caching_service}\n"
        f"Python Version: {python_version}\n"
        f"MySQL Version: {sql_version}\n"
        f"Ports: {ports}\n"
        " see all the fields above properly , if caching field is given or selected as none , dont use any if there only then use it"
        "Look at all the fielsds the entry point the dependencies the python version the sql version and the properly gie the accurate code"
        "No comments or any text just give accurate code"
        )

        # Kubernetes prompt text (if Kubernetes is selected)
        if container_orchestration == "Docker and Kubernetes":
            k8s_prompt_text = (
                "Generate Kubernetes YAML files (Deployment, Service, ConfigMap/Secret) "
                "for the same Flask application with the following details:\n"
                "No introduction, conclusion, or any extra text or paragraphs, just directly give the code.\n"
                f"Project Name: {project_name}\n"
                f"Description: {app_description}\n"
                f"Environment Variables: {env_vars}\n"
                f"Ports: {ports}\n"
                "Include configurations for persistence, load balancing, "
                "and auto-scaling if enabled."
                "No comments or any tect just give accurate code"
            )

        # Docker generation
        docker_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Generate a complete Dockerfile based on the following details:No extra details ,, no intro ,conclusion etc , give accurate and properly functional docker file for Flask application.leave the mysql part we can figure that out later ,, you please do Flask part only here in docker file"),
                ("human", docker_prompt_text),
            ]
        )
        docker_chain = docker_prompt | llm
        docker_output = docker_chain.invoke({"input": docker_prompt_text}).content

        # Docker Compose generation
        docker_compose_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Generate a Docker Compose file for this Flask project and MySQL.NO extra details introduction or extra texts , gove accurate properly functional code based on the prompt. for the cache part if none is selected means dont use , or else if something else is selcted and present in the cahce like redi so memchace or none then give its config as seen"),
                ("human", docker_compose_prompt_text),
            ]
        )
        docker_compose_chain = docker_compose_prompt | llm
        docker_compose_output = docker_compose_chain.invoke({"input": docker_compose_prompt_text}).content

        # Kubernetes generation (if selected)
        if container_orchestration == "Docker and Kubernetes":
            k8s_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "Generate Kubernetes YAMLs based on the following details:No extra details"),
                    ("human", k8s_prompt_text),
                ]
            )
            k8s_chain = k8s_prompt | llm
            k8s_output = k8s_chain.invoke({"input": k8s_prompt_text}).content

        # Display Docker output in code box
        if docker_output:
            st.markdown("### Dockerfile")
            st.code(docker_output, language='dockerfile')

        # Display Docker Compose output in code box (if applicable)
        if docker_compose_output:
            st.markdown("### Docker Compose")
            st.code(docker_compose_output, language='yaml')

        # Display Kubernetes output in code box (if selected)
        if k8s_output:
            st.markdown("### Kubernetes YAMLs")
            st.code(k8s_output, language='yaml')

        # Provide download buttons only for the generated files
        if docker_output:
            if st.download_button("Download Dockerfile", docker_output, file_name="Dockerfile"):
                st.success("Dockerfile downloaded successfully!")

        if docker_compose_output:
            if st.download_button("Download Docker Compose", docker_compose_output, file_name="docker-compose.yml"):
                st.success("Docker Compose file downloaded successfully!")

        if k8s_output:
            if st.download_button("Download Kubernetes YAML", k8s_output, file_name="kubernetes-deployment.yml"):
                st.success("Kubernetes YAML file downloaded successfully!")

        # Additional instructions for running the scripts
        st.markdown("### Instructions to Run the Generated Scripts:")
        st.markdown("""
        **For Docker:**
        1. Build the Docker image: `docker build -t <image_name> .`
        2. Run the container: `docker run -p 8000:8000 <image_name>`

        **For Docker Compose:**
        1. Run: `docker-compose up --build`

        **Keep you docker and docker-compose files under the root directory

        **For Kubernetes** (if applicable):
        1. Apply Kubernetes resources: `kubectl apply -f kubernetes-deployment.yml`
        2. Ensure services are running using: `kubectl get services`
        """)


