# 03 - 可观测与排障手册（Playbook）

## 目标

把“理论链路”落到“工程可观察”，快速判断故障在哪一层。

---

## A. 三段式快速定位

1. **Pod 是否存在？**  
   - 不存在：多半在 API Server admission/validation 或上游控制器创建阶段失败
2. **Pod 是否 Pending 且 `spec.nodeName` 为空？**  
   - 是：调度层问题（资源、约束、PVC 绑定等）
3. **Pod 有 `spec.nodeName` 但不 Running？**  
   - 是：Kubelet/CRI/CNI/CSI/镜像/配置阶段问题

---

## B. 高频命令清单

```bash
kubectl get events -n <ns> --sort-by=.lastTimestamp
kubectl describe deploy/<name> -n <ns>
kubectl describe rs/<name> -n <ns>
kubectl describe pod/<name> -n <ns>
kubectl get pod/<name> -n <ns> -o yaml
kubectl get quota,limitrange -n <ns>
kubectl get pvc,pv -n <ns>
kubectl apply -f xxx.yaml --dry-run=server -o yaml
```

---

## C. 典型故障到阶段映射

### C1. `Error creating: ... exceeded quota`

- 阶段：API Server Admission（ResourceQuota）
- 现象：Pod 不存在，RS 反复创建失败

### C2. `serviceaccount ... not found`

- 阶段：API Server Admission（ServiceAccount）
- 现象：Pod 不存在

### C3. `FailedScheduling` / `Insufficient cpu`

- 阶段：Scheduler
- 现象：Pod Pending，`nodeName` 为空

### C4. `pod has unbound immediate PersistentVolumeClaims`

- 阶段：Scheduler / 存储绑定
- 现象：Pod Pending，`nodeName` 可能为空

### C5. `FailedMount` / `CreateContainerConfigError`

- 阶段：Kubelet/CSI 或配置引用阶段
- 现象：Pod 已有 nodeName，但容器起不来

---

## D. 关键字段速查

### Pod

- `spec.nodeName`：是否已绑定节点
- `status.phase`：粗粒度状态
- `status.conditions[type=PodScheduled]`：是否调度成功
- `status.containerStatuses`：容器级失败原因

### Deployment

- `metadata.generation`
- `status.observedGeneration`
- `status.updatedReplicas/readyReplicas/availableReplicas`

### ReplicaSet

- `spec.replicas` vs `status.replicas`
- `metadata.ownerReferences`

### PVC

- `status.phase`：Pending/Bound
- `spec.volumeName`

---

## E. 推荐排障顺序（实战）

1. `kubectl get pod -n <ns> -o wide`
2. `kubectl describe pod/<pod> -n <ns>`
3. `kubectl get events -n <ns> --sort-by=.lastTimestamp`
4. 回看上游：`describe rs` -> `describe deploy`
5. 若涉及资源/策略：`get quota,limitrange,webhooks`
6. 若涉及存储：`get pvc,pv`, `describe pvc/pv`

---

## F. 学习练习建议

1. 人工触发 ResourceQuota 超限，观察事件与对象是否创建
2. 删除 ServiceAccount，再创建 Pod，观察失败层级
3. 构造调度失败（资源不足、taint、PVC pending）
4. 构造 kubelet 阶段失败（错误镜像、缺失 ConfigMap）

