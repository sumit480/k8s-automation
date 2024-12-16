#Creating a deployment using python kubernetes module
from kubernetes import client, config

config.load_kube_config()

#Creating deployment
def create_deployment(data):
    apps_v1 = client.AppsV1Api()
    deployment_manifest = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": data["name"], "namespace": data["namespace"]},
        "spec": {
            "replicas": data["replicas"],
            "selector": {"matchLabels": {"app": data["name"]}},
            "template": {
                "metadata": {"labels": {"app": data["name"]}},
                "spec": {
                    "containers": [
                        {
                            "name": data["name"],
                            "image": data["image"],
                            "ports": [{"containerPort": data["port"]}],
                            "resources": {
                                "requests": {
                                    "cpu": data["cpu_request"],
                                    "memory": data["memory_request"],
                                },
                                "limits": {
                                    "cpu": data["cpu_limit"],
                                    "memory": data["memory_limit"],
                                },
                            },
                        }
                    ]
                },
            },
        },
    }
    apps_v1.create_namespaced_deployment(
        namespace=data["namespace"], body=deployment_manifest
    )
    return data["name"]

#Get the status of a deployment
def get_deployment_status(namespace, name):
    apps_v1 = client.AppsV1Api()
    deployment = apps_v1.read_namespaced_deployment_status(name, namespace)
    replicas = deployment.status.replicas
    ready_replicas = deployment.status.ready_replicas
    return {
        "name": name,
        "namespace": namespace,
        "replicas": replicas,
        "ready_replicas": ready_replicas,
    }
