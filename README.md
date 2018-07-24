# Prometheus and Grafana Kubernetes Monitoring Setup

```
Kubernetes 1.8+
Grafana:5.0.1
Prometheus:v2.1.0
```

Apply 1:
```
kubectl apply -f namespace.yaml
kubectl apply -f prometheus/
kubectl apply -f prometheus/node-exporter/
kubectl apply -f prometheus/alertmanager/
kubectl apply -f prometheus/kube-state-metrics/
```

```
kubectl apply -f prometheus/pushgateway/
```

Generate Grafana certs and apply 2:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /tmp/tls.key -out /tmp/tls.crt
kubectl create secret --namespace monitoring  tls grafana-secret  --key /tmp/tls.key --cert /tmp/tls.crt

kubectl apply -f grafana/

```

Generic Graphite exporter
```
kubectl apply -f prometheus/graphite-exporter/
```

Import/Reimport dashboard assumes default password:
```
kubectl apply -f grafana/import-job

kubectl --namespace monitoring create configmap grafana-import-dashboards --from-file=grafana/dashboards/ -o json --dry-run | kubectl replace  -f -

kubectl --namespace monitoring delete job grafana-import-dashboards
kubectl apply -f grafana/import-job/job.yaml
```

Custom Metrics API
```
kubectl create namespace custom-metrics-adapter
kubectl create secret --namespace custom-metrics-adapter  tls cm-adapter-serving-certs  --key /tmp/tls.key --cert /tmp/tls.crt
kubectl apply -f custom-metrics-adapter/

kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1" | jq
```

# Change Grafana password!!!
Get grafana endpoint:
```
kubectl get svc  --namespace monitoring
```

- Configure Prometheus data source for Grafana:
`Grafana UI / Data Sources / Add data source`
  - `Name`: `prometheus`
  - `Type`: `Prometheus`
  - `Url`: `http://prometheus:9090`
  - `Add`
