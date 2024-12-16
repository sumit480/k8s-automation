from kubernetes import client

def create_service(data):
    """Create a service to expose the deployment."""
    core_v1 = client.CoreV1Api()
    service_manifest = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": data["name"], "namespace": data["namespace"]},
        "spec": {
            "selector": {"app": data["name"]},
            "ports": [{"port": data["port"], "targetPort": data["port"]}],
            "type": "LoadBalancer",
        },
    }
    core_v1.create_namespaced_service(namespace=data["namespace"], body=service_manifest)
