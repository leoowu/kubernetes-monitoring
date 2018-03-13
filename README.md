# Prometheus and Grafana Kubernetes Monitoring Setup

```
Kubernetes 1.8+
Grafana:5.0.1
Prometheus:v2.1.0
```

Apply:
```
kubectl apply -f namespace.yaml
kubectl apply -f prometheus/
kubectl apply -f prometheus/node-exporter/
kubectl apply -f prometheus/kube-state-metrics/
kubectl apply -f prometheus/graphite-exporter/
kubectl apply -f grafana/
```

Generate Grafana certs:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /tmp/tls.key -out /tmp/tls.crt   
kubectl create secret --namespace monitoring  tls grafana-secret  --key /tmp/tls.key --cert /tmp/tls.crt
```

Other:
```
kubectl get svc  --namespace monitoring
```

- Configure Prometheus data source for Grafana:
`Grafana UI / Data Sources / Add data source`
  - `Name`: `prometheus`
  - `Type`: `Prometheus`
  - `Url`: `http://prometheus:9090`
  - `Add`
