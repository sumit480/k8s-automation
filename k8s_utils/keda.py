from kubernetes import client

def configure_keda(data):
    """Configure KEDA for event-driven autoscaling."""
    custom_api = client.CustomObjectsApi()
    keda_scaled_object = {
        "apiVersion": "keda.sh/v1alpha1",
        "kind": "ScaledObject",
        "metadata": {"name": f"{data['name']}-scaledobject", "namespace": data["namespace"]},
        "spec": {
            "scaleTargetRef": {"name": data["name"]},
            "pollingInterval": 30,
            "cooldownPeriod": 300,
            "triggers": [
                {
                    "type": data["event_source"]["type"],
                    "metadata": data["event_source"]["metadata"],
                }
            ],
        },
    }
    custom_api.create_namespaced_custom_object(
        group="keda.sh",
        version="v1alpha1",
        namespace=data["namespace"],
        plural="scaledobjects",
        body=keda_scaled_object,
    )
