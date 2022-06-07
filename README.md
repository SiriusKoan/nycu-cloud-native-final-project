# nycu-cloud-native-final-project
## Setup
Setup argocd.
```
$ bash setup-argocd.sh
```

Setup grafana for monitoring and crawler application.
```
$ kubectl apply -f applications/crawler-app.yaml
$ kubectl apply -f applications/grafana.yaml
```

## Usage
Since this application is only for internal use, so we use port-forwarding to expose the service.
```
$ kubectl port-forward -n cloudnative svc/crawler-service 8080:5000
```

Get the result. The whole process take about 1 minute.
```
$ curl localhost:8080/run -o result.xlsx
```

If the server returns errors, try to curl `/test` to check whether the server is alive.
```
$ curl localhost:8080/test
```
