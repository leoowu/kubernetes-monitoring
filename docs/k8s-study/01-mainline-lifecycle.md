# 01 - Kubernetes 主链路：Pod 生命周期（Mainline）

## 1. 目标

掌握从 `kubectl apply` 到 Pod 可运行（再到删除）的主链路控制流与数据流。

---

## 2. 主链路总览

```text
kubectl/apply
  -> kube-apiserver
  -> etcd (对象持久化)
  -> Deployment Controller
  -> ReplicaSet Controller
  -> Pod object created
  -> Scheduler bind node
  -> Kubelet create sandbox/container
  -> Pod Running/Ready
  -> Service/EndpointSlice 生效
  -> 删除时 graceful termination + GC
```

---

## 3. Step by Step

### Step 1: API Server 接收并处理请求

- 处理链：AuthN -> AuthZ -> Admission -> Defaulting -> Validation -> Persist
- 结果：对象写入 etcd，产生 `resourceVersion`

### Step 2: Deployment Controller 创建/更新 ReplicaSet

- Deployment template 变化会生成新 RS（hash）
- Deployment 不直接创建 Pod

### Step 3: ReplicaSet Controller 创建 Pod

- 基于 `spec.template` 实例化 Pod
- 设置 `ownerReferences` 指向 ReplicaSet
- Pod 初始通常 `Pending`

### Step 4: Scheduler 调度

- 处理 `spec.nodeName` 为空的 Pod
- 阶段：Queue -> Filter -> Score -> Bind
- 结果：Pod 写入 `spec.nodeName`

### Step 5: Kubelet 落地运行（待继续深入）

- 监听分配到本节点的 Pod
- 调用 CRI/CNI/CSI
- 先 initContainer，再主容器/sidecar

### Step 6: 健康检查与流量接入（待继续深入）

- readiness/liveness 影响 Service 后端与流量路由

### Step 7: 删除与回收（待继续深入）

- preStop/SIGTERM/grace period/SIGKILL
- finalizer 与 GC 协同

---

## 4. 最小观察命令

```bash
kubectl get deploy,rs,pod -n <ns> -w
kubectl describe deploy/<name> -n <ns>
kubectl describe rs/<name> -n <ns>
kubectl describe pod/<name> -n <ns>
kubectl get events -n <ns> --sort-by=.lastTimestamp
```

