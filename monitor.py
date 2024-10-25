from kubernetes import client, config
import time

# Load the Kubernetes configuration
config.load_kube_config()  # Use load_incluster_config() if running inside the cluster

# Constants
DEPLOYMENT_NAME = 'my-app'
NAMESPACE = 'default'  # Change if necessary
TARGET_CPU_PERCENTAGE = 50  # Target CPU usage percentage
MIN_REPLICAS = 1  # Minimum number of replicas
MAX_REPLICAS = 5  # Maximum number of replicas

# Create API clients
apps_v1 = client.AppsV1Api()
metrics_v1 = client.CustomObjectsApi()

def get_cpu_usage(pod_name):
    """Retrieve the CPU usage of the specified pod."""
    try:
        metrics = metrics_v1.get_namespaced_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            namespace=NAMESPACE,
            plural="pods",
            name=pod_name
        )
        
        # Check if the metrics contain containers
        if 'containers' in metrics and len(metrics['containers']) > 0:
            usage = metrics['containers'][0]['usage'].get('cpu', '')
            if usage:
                # Convert the usage to an integer
                if usage.endswith('n'):  # nano cores
                    return int(usage[:-1]) // 1000000  # Convert to millicores
                elif usage.endswith('m'):  # millicores
                    return int(usage[:-1])  # Return as is
                elif usage.endswith('k'):  # kilocores
                    return int(usage[:-1]) * 1000  # Convert to millicores
                elif usage.endswith(''):  # no unit, unexpected
                    return 0
            else:
                print(f"No CPU usage found for pod {pod_name}.")
                return 0  # No usage found
        else:
            print(f"No container metrics available for pod {pod_name}.")
            return 0  # No container metrics
        
    except Exception as e:
        print(f"Error fetching CPU usage for pod {pod_name}: {e}")
        return 0  # Return 0 if there's an error

def scale_deployment(replicas):
    """Scale the deployment to the specified number of replicas."""
    deployment = apps_v1.read_namespaced_deployment(DEPLOYMENT_NAME, NAMESPACE)
    deployment.spec.replicas = replicas
    apps_v1.patch_namespaced_deployment(DEPLOYMENT_NAME, NAMESPACE, deployment)
    print(f"Scaled deployment {DEPLOYMENT_NAME} to {replicas} replicas.")

def get_pod_names():
    """Retrieve the names of the pods for the deployment."""
    pods = client.CoreV1Api().list_namespaced_pod(NAMESPACE, label_selector=f'app={DEPLOYMENT_NAME}')
    return [pod.metadata.name for pod in pods.items if pod.metadata.labels.get('app') == DEPLOYMENT_NAME]

def main():
    while True:
        # Get the list of pods for the specific deployment
        pod_names = get_pod_names()
        
        if not pod_names:  # Check if there are no pods
            print(f"No pods found for deployment {DEPLOYMENT_NAME}.")
            time.sleep(10)  # Wait before retrying
            continue

        # Calculate average CPU usage
        total_cpu_usage = 0
        for pod_name in pod_names:
            cpu_usage = get_cpu_usage(pod_name)
            total_cpu_usage += cpu_usage

        average_cpu_usage = total_cpu_usage / len(pod_names) if pod_names else 0

        print(f"Average CPU Usage: {average_cpu_usage}%")

        # Scaling logic
        current_replicas = len(pod_names)
        if average_cpu_usage > TARGET_CPU_PERCENTAGE and current_replicas < MAX_REPLICAS:
            scale_deployment(current_replicas + 1)
        elif average_cpu_usage < TARGET_CPU_PERCENTAGE and current_replicas > MIN_REPLICAS:
            scale_deployment(current_replicas - 1)

        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    main()
