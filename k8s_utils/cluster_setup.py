import subprocess

def install_helm():
    subprocess.run(["helm", "version"], check=True)

def install_keda():
    subprocess.run([
        "helm", "repo", "add", "kedacore", "https://kedacore.github.io/charts"
    ], check=True)
    subprocess.run(["helm", "repo", "update"], check=True)
    subprocess.run([
        "helm", "install", "keda", "kedacore/keda", "--namespace", "keda",
        "--create-namespace"
    ], check=True)

def verify_cluster_setup():
    keda_status = subprocess.run(
        ["kubectl", "get", "pods", "-n", "keda"], capture_output=True, text=True
    )
    return keda_status.stdout
