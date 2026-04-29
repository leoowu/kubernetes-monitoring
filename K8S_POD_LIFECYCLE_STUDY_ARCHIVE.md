# Kubernetes Pod 生命周期与调度策略学习归档（会话完整版）

> 文档目的：将本次会话中的核心知识、推理路径、工程观察方法、实操命令与扩展方案完整归档，作为后续持续维护的学习底座。  
> 读完并按步骤实操后，应能独立解释并观测 Kubernetes Pod 生命周期与关键控制面机制。

---

## 0. 学习目标与成果定义

### 0.1 学习目标

1. 彻底掌握 Pod 从创建到删除的生命周期。
2. 明确 API Server、etcd、Scheduler、Controller、Kubelet 的职责边界与交互方式。
3. 掌握对象层（Deployment/ReplicaSet/Pod/PVC/ConfigMap/Ingress/ServiceAccount）与运行时层（CRI/CNI/CSI）的关系。
4. 能从工程视角定位问题：发生在 API Server、Scheduler、还是 Kubelet/存储/网络阶段。
5. 能设计并落地「业务 Leader 分布约束」策略（Scheduler Plugin 或 Operator 方案）。

### 0.2 成果判定（你学完应能做到）

- 能手写并解释 `kubectl apply` 后每个阶段发生了什么。
- 能解释 `resourceVersion` 与 etcd revision 的关系与差异。
- 能解释 `ownerReferences`、adoption、GC 的逻辑。
- 能用 `kubectl get/describe/events` 在 5 分钟内定位 Pod 卡住阶段。
- 能给出动态 Leader 场景下的可运行方案（Operator + 调度约束 + leader transfer）。

---

## 1. 本次会话的重点主题（按出现顺序归档）

1. Pod 全生命周期（包含 etcd 对象变化、状态变化、组件交互）
2. API Server 请求链路细化（Authentication/Authorization/Admission/Defaulting/Validation）
3. 数据流与控制流分离分析（协议、URL、payload、watch）
4. 用户可观测性与排障路径（怎么看、在哪看、失败表现）
5. Deployment/ReplicaSet/Pod 结构设计与 rollout 机制
6. ownerReferences 与 selector 的区别、adoption 逻辑
7. ResourceQuota / ServiceAccount / PVC 失败分层
8. ServiceAccount projected volume 与 AWS STS（IRSA）token 逻辑
9. Scheduler Filter 思路与 Leader 分布约束设计
10. Operator 打标签 + 原生调度规避方案

---

## 2. 总体架构心智模型（必须先建立）

Kubernetes 协作主模式：

```text
组件 watch API Server -> 发现对象变化 -> 执行本组件职责 -> 更新对象到 API Server -> API Server 持久化到 etcd
```

关键原则：

1. 多数组件不直接互相 RPC，而是通过 API 对象协作。
2. API Server 是统一入口与一致性边界。
3. etcd 是状态事实存储（源数据）。
4. Controller 是持续收敛，不是一次性执行。

---

## 3. 示例对象清单（会话中用于讲解的完整业务场景）

示例应用包含：

- Ingress
- Service
- Deployment（Java 主容器 + sidecar）
- initContainer
- ConfigMap
- PVC
- shared volume（emptyDir）
- ServiceAccount

对象创建顺序可理解为：

```text
Namespace -> ServiceAccount -> ConfigMap -> PVC -> Deployment -> Service -> Ingress
```

> 注意：创建 Deployment 不等于立刻创建 Pod，Pod 由后续控制器产生。

---

## 4. API Server 写入前链路（精讲）

逻辑顺序：

```text
Authentication -> Authorization -> Admission -> Defaulting -> Validation -> Persist(etcd)
```

### 4.1 Authentication（认证：你是谁）

- 输入：token/cert/OIDC/SA token
- 输出：user/groups 身份上下文

### 4.2 Authorization（鉴权：你能不能做）

- 常用：RBAC
- 判定维度：verb + resource + namespace + identity

### 4.3 Admission（准入：你的对象内容是否可接受/需改写）

- Mutating：可改对象（注入 sidecar、补字段）
- Validating：只能拒绝/放行

### 4.4 Defaulting（默认值填充）

补齐未显式填写字段（如 restartPolicy、schedulerName 等）。

### 4.5 Validation（API 语义校验）

确保对象结构与语义合法（selector/template 匹配等）。

### 4.6 Persist（写 etcd）

通过 API Server storage 层写入 etcd，生成新的版本。

---

## 5. resourceVersion 与 etcd revision（会话重点）

### 5.1 核心结论

- etcd revision：存储层 MVCC 版本（etcd 内部语义）
- resourceVersion：Kubernetes API 层版本游标（对客户端 opaque）

### 5.2 为什么不直接统一暴露 etcd revision

1. API 层需要与存储实现解耦。
2. watch cache/聚合 API/扩展机制不应暴露底层细节。
3. 客户端应依赖稳定 API 语义，而非 etcd 内部行为。

---

## 6. Deployment -> ReplicaSet -> Pod（控制链路）

### 6.1 为什么 Deployment 不直接创建 Pod

- Deployment 负责发布策略（rollout/rollback/history）
- ReplicaSet 负责副本收敛
- Pod 是运行实例

### 6.2 两层 spec 的设计（你重点问过）

`ReplicaSet.spec`：控制器意图（replicas/selector/template）  
`ReplicaSet.spec.template.spec`：被创建对象（Pod）的规格。

这是一种“控制意图”与“对象模板”分离设计。

### 6.3 rollout 过程（RollingUpdate）

以 image 变更触发：

1. Deployment template 变化 -> 新 hash -> 新 ReplicaSet
2. 新 RS 扩容，旧 RS 缩容
3. 按 maxSurge/maxUnavailable 逐步替换
4. Deployment status 持续更新直到完成

---

## 7. ownerReferences、selector、adoption（高频易混）

### 7.1 三者职责

- selector：匹配集合（谁“看起来”属于我）
- ownerReferences：所有权（谁“正式”归我管）
- controller=true：唯一控制器 owner

### 7.2 删除 Pod ownerReferences 后会怎样

- Pod 不会立即被删除（无 owner 不等于要被 GC）
- 若 label 仍匹配某 RS，RS Controller 可能 adopt 回来
- adopt 时填入的 owner 是 ReplicaSet，不是 Deployment

---

## 8. Scheduler 阶段（Pod Pending -> 绑定 Node）

### 8.1 输入条件

- Pod 已存在
- `spec.nodeName` 为空
- `schedulerName` 匹配当前调度器

### 8.2 关键流程

```text
Queue -> Filter -> Score -> Bind
```

Bind 后 Pod 出现 `spec.nodeName`，但容器尚未运行。

### 8.3 常见失败信号

- `FailedScheduling`
- `Insufficient cpu/memory`
- `untolerated taint`
- `pod has unbound immediate PersistentVolumeClaims`

---

## 9. ResourceQuota / ServiceAccount / PVC 失败分层（会话结论）

### 9.1 ResourceQuota

- 主要在 API Server admission 阶段拦截
- 失败时 Pod 不会创建

### 9.2 ServiceAccount

- 主要在 API Server admission 阶段处理
- SA 不存在常导致 Pod 创建被拒绝

### 9.3 PVC

跨阶段：

- Pod 创建时通常只记录引用，不一定强阻断
- Scheduler 可能因 PVC 未绑定而卡住
- Kubelet/CSI 可能在挂载阶段失败

---

## 10. projected volume 与 ServiceAccount token（你给的 YAML 深挖）

会话中拆解了两类 token：

1. `kube-api-access-*`：访问 Kubernetes API 的默认凭据（token + ca.crt + namespace）
2. `aws-iam-token`：面向 STS 的 audience token（IRSA 场景）

关键逻辑：

- kubelet 通过 TokenRequest 向 API Server 申请短期 token
- token 有过期与轮转
- Kubernetes 权限由 RBAC 决定
- AWS 权限由 IAM trust/role 决定

---

## 11. 动态 Leader 约束设计（会话后半核心）

你的约束从“同节点不共 Leader”到“每节点最多 2 个 Leader”逐步演进。

### 11.1 结论

若 Leader 是运行时选举结果，不能只靠原生 Scheduler 一次性保证。

需要两层：

1. 调度时约束（新/重建 Pod）
2. 运行时修正（角色变化后）

### 11.2 两种实现路线

#### 路线 A：Scheduler Filter Plugin

- Filter 阶段统计候选 Node 当前 leader 数
- 若 `>= max` 则拒绝该 Node
- 可配合 Reserve/Unreserve 处理并发调度

#### 路线 B：Operator + Node Label + nodeAffinity（你提出的方案）

- Operator 统计每个 Node 的 leader 数
- leader 满载 Node 打 label（如 `leader-full=true`）
- Pod 使用 nodeAffinity 规避
- 运行时冲突由 Operator 执行 leader transfer 修正

> 工程实践中该路线维护成本更低，适合大多数团队。

---

## 12. 可观测与排障总表（实操必备）

### 12.1 分层定位法

1. Pod 不存在 -> API Server admission/validation 或上游 controller 创建失败
2. Pod Pending 且 nodeName 为空 -> Scheduler/资源/约束/PVC
3. Pod 有 nodeName 但未 Running -> Kubelet/CRI/CNI/CSI/镜像/配置

### 12.2 高频命令

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

## 13. 按步骤学习路径（Step by Step）

### Step 1：请求入站与 API Server 处理

目标：看懂 authn/authz/admission/defaulting/validation。

### Step 2：Deployment 创建 RS

目标：理解 rollout 起点、hash、ownerReferences。

### Step 3：RS 创建 Pod

目标：理解 template 实例化与 Pod 初始状态。

### Step 4：Scheduler 绑定 Node

目标：看懂 Filter/Score/Bind 与调度失败事件。

### Step 5：Kubelet 实例化 Pod（建议下一轮继续）

目标：CRI/CNI/CSI、initContainer、sidecar 顺序。

### Step 6：健康检查与流量接入

目标：readiness/liveness 对 Service/EndpointSlice 影响。

### Step 7：删除与回收

目标：graceful termination、finalizer、GC。

### Step 8：业务约束扩展

目标：Leader 分布约束（Plugin vs Operator）与最终一致性策略。

---

## 14. 后续维护规范（建议）

建议将文档拆分为 4 个长期维护文件：

1. `01-mainline-lifecycle.md`
2. `02-apiserver-admission-policy.md`
3. `03-observability-debug-playbook.md`
4. `04-jraft-leader-scheduling-strategy.md`

每次新增内容固定追加：

1. 新概念定义
2. 交互图（控制流+数据流）
3. 可观测命令
4. 故障样例与定位路径
5. 设计权衡

---

## 15. 本次会话“你的关键问题”归档（便于复盘思路）

1. 要求“完整 Pod 生命周期 + 组件级细节 + 对象更新细节”
2. 要求“不要比喻，要严谨表达”
3. 要求“给协议、URL、payload 级别的交互信息”
4. 追问“resourceVersion 与 revision 为什么不同”
5. 强调“从用户可观察角度看数据流和逻辑流”
6. 深问“rollout、ownerReferences、adoption 的细节”
7. 深问“ResourceQuota/ServiceAccount/PVC 在哪个阶段失败”
8. 提供 projected volume 案例，追问 token 挂载与工作机制
9. 深入 JRaft Leader 跨 Node 约束设计与实现路径

---

## 16. 建议下一次继续学习的主题（承接本会话）

1. Kubelet syncPod 详细链路
2. CRI 调用与 sandbox/container 生命周期
3. CNI 数据面与 Pod 网络连通
4. CSI attach/mount 失败树
5. Pod 状态字段精确语义（phase vs conditions vs containerStatuses）
6. 删除路径（preStop、SIGTERM、grace period、SIGKILL）

---

## 17. 归档说明

本文件已在本地工作区创建：  
`/workspace/K8S_POD_LIFECYCLE_STUDY_ARCHIVE.md`

你可以：

1. 直接下载此文件到本地电脑归档；
2. 后续在此文件上持续增量维护；
3. 按第 14 节拆分成专题文档，形成长期学习库。

