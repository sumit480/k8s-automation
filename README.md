# Kubernetes Automation Tool
This project provides a Flask API to automate operations on a bare Kubernetes cluster, including setup, deployment creation, event-driven scaling with KEDA, and health monitoring of deployments. The tool is modular, scalable, and adheres to best practices for Kubernetes resource management and API design.

## Features
   1. **Cluster Setup:** Install required tools like Helm and KEDA to configure the Kubernetes cluster.
   2. **Deploy Applications:** Create deployments with configurable CPU, memory, and autoscaling policies.
   3. **Event-Driven Autoscaling:** Integrate with KEDA for custom metrics and event-driven scaling.
   4. **Health Monitoring:** Retrieve the health status of a deployment, including resource usage and pod status.
   5. **Security:** Validate inputs and enforce error handling to prevent misconfigurations.
   6. **Modularity:** Functions are designed to be reusable and extensible for different Kubernetes workloads.
## Prerequisites
   1. **Kubernetes Cluster:** A working Kubernetes cluster with kubectl access configured.
   2. **Helm Installed:** Ensure helm is installed and configured.
   3. **Python:** Python 3.9+ is required.
   4. **Kubernetes Python Client:** Installed as part of the tool dependencies.
   5. **Docker:** For containerizing the app.
## Installation

1. ### Clone the Repository

```bash
git clone <repository-url>
cd kubernetes-automation-tool
```

2. ### Install Dependencies
Use the provided requirements.txt:

```bash
pip install -r requirements.txt
```
3. ### Configure Kubernetes Access
Ensure the Kubernetes kubeconfig file is correctly set up:

```bash
kubectl config view
```
4. ### Run the Flask Application

```bash
python app.py
The app will run on http://127.0.0.1:5000 by default.
```
## Endpoints
1. ### Cluster Setup
* **Endpoint:** `/setup`
* **Method:** `POST`
* **Description:** Installs Helm and KEDA on the cluster.
* **Example:**
```bash
curl -X POST http://127.0.0.1:5000/setup
```
2. ### Create Deployment
* **Endpoint:** `/deploy`
* **Method:** `POST`
* **Payload:**
```json
{
  "name": "my-deployment",
  "namespace": "default",
  "image": "nginx:latest",
  "replicas": 2,
  "port": 80,
  "cpu_request": "100m",
  "cpu_limit": "500m",
  "memory_request": "128Mi",
  "memory_limit": "256Mi",
  "min_replicas": 1,
  "max_replicas": 5,
  "event_source": {
    "type": "kafka",
    "metadata": {
      "bootstrapServers": "my-kafka-broker:9092",
      "topic": "my-topic",
      "consumerGroup": "my-consumer-group"
    }
  }
}
```

Example:
```bash
curl -X POST http://127.0.0.1:5000/deploy \
     -H "Content-Type: application/json" \
     -d '{...}'
```
3. ### Check Deployment Status
   * **Endpoint:** `/status/<namespace>/<name>`
   * **Method:** `GET`
   * **Example:**
```bash
curl -X GET http://127.0.0.1:5000/status/default/my-deployment
```
## Configuration
Modify the Kubernetes cluster access via `~/.kube/config` if needed.
Customize the Flask app settings (e.g., host, port) in `app.py`.

## Error Handling
The API validates inputs and returns meaningful error messages, e.g.:

   * `400`: Bad Request (invalid payload)
   * `403`: Forbidden (conflict between HPA and KEDA)
   * `500`: Internal Server Error (unexpected issues)

## Dockerization
### Dockerfile
```dockerfile
## Base image
FROM python:3.9-slim

## Set working directory
WORKDIR /app

## Copy application code
COPY . /app

## Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

## Expose the application port
EXPOSE 5000

## Run the Flask app
CMD ["python", "app.py"]
```

## Build and Run Docker Image
### Build the Docker Image:

```bash
docker build -t kubernetes-automation-tool .
```

### Run the Docker Container:

```bash
docker run -d -p 5000:5000 kubernetes-automation-tool
```
## Design Choices
   1. **Modularity:** Functions are divided into separate modules (setup.py, deployment.py, etc.).
   2. **Scalability:** Event-driven scaling with KEDA allows flexibility for various workloads. 
   3. **Error Handling:** Used `try-catch` block for robust error handling ensures a reliable user experience and capture application errors effectively.

## CI/CD using gitlab

### Environment Variables
You need to configure the following environment variables in the CI/CD pipeline environment:

1. **AWS Credentials:**

   * `AWS_ACCESS_KEY_ID:` Your AWS access key.
   * `AWS_SECRET_ACCESS_KEY:` Your AWS secret access key.
   * `AWS_REGION:` Your AWS region (e.g., us-east-1).

2. **EKS and ECR Configuration:**

   * `ECR_REPO:` The ECR repository URI.
   * `K8S_NAMESPACE:` Namespace for your Kubernetes deployment.

### Key Steps in the Pipeline
#### Build Stage:

   Builds the Docker image using the tool's source code.
   Pushes the image to an ECR repository using AWS CLI.

#### Deploy Stage:

   Uses aws eks CLI to configure access to the EKS cluster.
   Updates the Kubernetes deployment manifest with the latest Docker image.
   Applies the Kubernetes deployment and service configuration using kubectl.

### Permissions Required
1. **IAM Role for CI/CD User: We can use OIDC configuration to Authenticate for AWS Resources** 

    * `ECR Access:` AmazonEC2ContainerRegistryFullAccess.
    * `EKS Access:` AmazonEKSClusterPolicy, AmazonEKSWorkerNodePolicy.
    * `S3 Access:` (Optional) If required for kubeconfig or other dependencies.
2. **Kubernetes Role:**

    Configure an RBAC role for the CI/CD user to have permission to deploy resources.

## Security Considerations
   * Ensure the Kubernetes API server is accessible only from trusted sources.
   * Avoid hardcoding sensitive credentials (e.g., Kafka details).
   * Use role-based access control (RBAC) to limit API access.

## Future Improvements
   * Add support for more event sources (e.g., Databases etc).
   * Enhance observability with metrics dashboards.


## Author:
[Sumit Gupta] (https://github.com/sumit480)