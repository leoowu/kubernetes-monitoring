# Prometheus and Grafana Kubernetes Monitoring Setup


```
Kubernetes 1.12 +
Grafana:5.3.0
Prometheus:v2.4.3
```


Apply 1:
```
kubectl apply -f namespace.yaml
kubectl apply -f prometheus/
kubectl apply -f prometheus/node-exporter/
kubectl apply -f prometheus/kube-state-metrics/
```


Grafana
```
kubectl apply -f grafana/
kubectl --namespace grafana create configmap grafana-import-dashboards --from-file=grafana/dashboards/ -o json --dry-run | kubectl replace  -f -
kubectl apply -f grafana/import-job/job.yaml

kubectl delete -f grafana/import-job/job.yaml
```


Other:
```
kubectl apply -f prometheus/pushgateway/
kubectl apply -f prometheus/alertmanager/
kubectl apply -f prometheus/graphite-exporter/
```


Custom Metrics API
```
kubectl create namespace custom-metrics-adapter
kubectl create secret --namespace custom-metrics-adapter  tls cm-adapter-serving-certs  --key /tmp/tls.key --cert /tmp/tls.crt
kubectl apply -f custom-metrics-adapter/

kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1" | jq
```


Grafana certs:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /tmp/tls.key -out /tmp/tls.crt
kubectl create secret --namespace grafana  tls grafana-secret  --key /tmp/tls.key --cert /tmp/tls.crt

kubectl apply -f grafana/
```
