# 02 - API Server 准入与策略学习手册

> 本文聚焦 API Server 请求链路中的“检查与治理”层：Authentication、Authorization、Admission、Defaulting、Validation。

---

## 1. 请求链路总览

```text
Client -> kube-apiserver
  -> Authentication
  -> Authorization
  -> Admission (Mutating/Validating)
  -> Defaulting
  -> Validation
  -> Persist to etcd
```

---

## 2. Authentication（你是谁）

常见来源：

- client certificate
- bearer token
- OIDC token
- service account token

产出：`user + groups`。

---

## 3. Authorization（你能做什么）

常见实现：RBAC。

判定维度：

- verb（create/get/update/delete/watch...）
- resource（pods/deployments...）
- scope（namespace / cluster）
- user/groups/serviceaccount

---

## 4. Admission（对象是否合规，是否需要改写）

### 4.1 Mutating Admission

可修改对象：

- 注入 sidecar
- 补默认资源
- 添加标签/注解

### 4.2 Validating Admission

只做放行/拒绝：

- 禁止 privileged
- 限制镜像仓库
- 限制 Ingress Host

---

## 5. Defaulting（默认值填充）

示例：

- `restartPolicy: Always`
- `schedulerName: default-scheduler`
- `dnsPolicy: ClusterFirst`

---

## 6. Validation（API 语义校验）

示例：

- Deployment selector 必须匹配 template labels
- volumeMount 引用的 volume 必须存在
- 字段类型/范围合法

---

## 7. 重点策略对象

### 7.1 ResourceQuota

- 准入时检查配额是否超限
- 超限会拒绝请求（对象不入库）
- Quota Controller 持续维护 `status.used`

### 7.2 LimitRange

- 单对象资源边界（min/max/default/defaultRequest）
- 可自动补 requests/limits

### 7.3 ServiceAccount Admission

- 校验 SA 是否存在
- 注入 projected token/ca/namespace

### 7.4 PodSecurity / Webhook

- 强制安全策略
- 企业定制策略扩展

---

## 8. `resourceVersion` vs etcd revision

结论：

- etcd revision：存储层 MVCC 版本
- resourceVersion：Kubernetes API 层游标（opaque）

设计原因：API 与存储实现解耦，便于缓存、聚合、扩展演进。

---

## 9. 可观测命令

```bash
kubectl apply -f app.yaml --dry-run=server -o yaml
kubectl get quota,limitrange -n <ns>
kubectl describe quota <name> -n <ns>
kubectl get validatingwebhookconfigurations
kubectl get mutatingwebhookconfigurations
kubectl get ns <ns> -o yaml
```

---

## 10. 快速定位规则

- `kubectl apply` 直接报错：多半是 admission/validation/authz
- 对象不存在：多半未通过 API Server 检查
- ReplicaSet 有但 Pod 无：创建 Pod 被 API Server 拒绝（quota/SA/webhook 常见）
