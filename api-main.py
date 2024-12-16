from flask import Flask, request, jsonify
from k8s_utils import cluster_setup, deployment, service, keda

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200


@app.route('/setup', methods=['POST'])
def setup_cluster():
    try:
        cluster_setup.install_helm()
        cluster_setup.install_keda()
        status = cluster_setup.verify_cluster_setup()
        return jsonify({"message": "Cluster setup completed.", "status": status}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deploy', methods=['POST'])
def create_deployment():
    try:
        data = request.get_json()
        deployment_name = deployment.create_deployment(data)
        service.create_service(data)
        keda.configure_keda(data)
        return jsonify({"message": "Deployment successfully created.", "deployment_name": deployment_name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status/<namespace>/<name>', methods=['GET'])
def get_status(namespace, name):
    try:
        status = deployment.get_deployment_status(namespace, name)
        return jsonify(status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = '5000' )
