# k8s-job-function
Trigger a k8s job via an API call with some body parameters to pass values to the job as arguments.

## Build image
```
docker build -t api-endpoint:v2.0.1 .
```
## Deploy api-service deployment
update image tag which you just built in deployment file 
```
kubectl create -f api-service.yaml
```
## Grant job create RBAC access 
grant job create rbac access to the default service account in particular namespace
```
kubectl create -f job-creator.yaml
kubectl create -f job-creator-rolebinding.yaml
```
## Port-forward api-service (local purpose)
```
kubectl port-forward svc/api-service 3000
```
## Trigger a k8s job via api call
```
curl -X POST 'http://127.0.0.1:3000/test' --header 'Content-Type: application/json' --data '{"q1": "abc","q2": "xyz"}'
```
