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
$ kubectl apply -f applications/prometheus.yaml
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

If you want to run it automatically, put this script to cronjob.
```
kubectl port-forward -n cloudnative svc/crawler-service 8080:5000
curl localhost:8080/run -o /home/user/result.xlsx
kill $(ps aux | grep port-forward | awk '{print $2}'
```

## Customization
If you want to update to code, please re-build the Docker image and push it to docker image registry.
```
$ docker build . -t {account}/{image}
$ docker push {account}/{image}
```

And you should remember to update the image field in `docker-compose.yaml` as well.

## Test
Run test.
```
$ pytest
```

Get test coverage.
```
$ python -m pytest . tests --doctest-modules --junitxml=test-results.xml
```

## Infrastructure Diagram
![image](https://user-images.githubusercontent.com/26023540/173837114-caeeda99-f437-4d8a-8028-8195860cbce7.png)
