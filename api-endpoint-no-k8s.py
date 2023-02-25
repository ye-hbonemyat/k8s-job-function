from kubernetes import client, config
import time

# Load Kubernetes configuration
config.load_kube_config()

# Create a BatchV1Api client
batchv1 = client.BatchV1Api()

# Define the function to create a Job
def create_job(job_name, arg1, arg2):
    # Define the Job configuration
    job_metadata = client.V1ObjectMeta(name=job_name)
    job_container = client.V1Container(name="my-container", image="busybox", command=['sh', '-c', f'echo "Running job with args {arg1} {arg2}"'])
    job_template = client.V1PodTemplateSpec(metadata=job_metadata, spec=client.V1PodSpec(restart_policy="Never", containers=[job_container]))
    job_spec = client.V1JobSpec(template=job_template, backoff_limit=0)
    job = client.V1Job(api_version="batch/v1", kind="Job", metadata=job_metadata, spec=job_spec)

    # Create the Job with a unique name
    while True:
        try:
            batchv1.create_namespaced_job(namespace="dev", body=job)
            print("Job created successfully with name: {}".format(job_metadata.name))
            break
        except client.rest.ApiException as e:
            if e.status == 409:
                # If the Job already exists, modify the name and retry creating the Job
                job_metadata.name = "test-job-{}".format(int(time.time()))
                job.metadata = job_metadata
                print("Job name already exists, creating new Job with name: {}".format(job_metadata.name))
            else:
                # If an unexpected error occurs, raise the exception
                raise e

# Define the function to handle the API request
def handle_request(request):
    if request.method == "POST":
        data = request.json
        if "q1" in data and "q2" in data:
            job_name = "my-job-{}".format(int(time.time()))
            create_job(job_name, data["q1"], data["q2"])
            return "Job created successfully with name: {}".format(job_name), 200
        else:
            return "Missing q1 or q2 parameter", 400
    else:
        return "Unsupported HTTP method", 405

# Define the Flask app and run it
from flask import Flask, request
app = Flask(__name__)
@app.route("/test", methods=["POST"])
def test():
    return handle_request(request)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
