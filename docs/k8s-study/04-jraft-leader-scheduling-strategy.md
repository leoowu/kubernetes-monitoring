# 04 - JRaft Leader 调度与分布策略（动态 Leader 场景）

> 目标：解决“Leader 是运行时选举结果”时的跨 Node 分布约束问题。

---

## 1. 问题定义

业务背景（会话场景）：

- 多个 StatefulSet（A/B/C/D...），每个 shard 3 副本（1 leader + 2 follower）
- Leader 不固定为 ordinal 0，可通过业务 API 查询当前 leader ordinal

常见约束演进：

1. 不允许任意两个 shard 的 leader 在同一 node
2. 每个 node 最多 1 个 leader
3. 每个 node 最多 2 个 leader（后续演进）

---

## 2. 核心现实：为什么不能只靠原生 Scheduler

Scheduler 只对 Pending Pod 做决策：

```text
Pending -> Filter/Score/Bind -> nodeName 写入
```

但动态 Leader 是运行后才变化：

```text
Pod 先 Running
-> JRaft 选举变化
-> follower 变 leader
```

这不是调度事件，Scheduler 不会自动“重排已运行 Pod”。

因此：

```text
调度时约束 + 运行时修正
```

必须同时存在。

---

## 3. 两条可落地路线

### 路线 A：Scheduler Framework Filter Plugin（强约束）

Filter 阶段检查候选 Node 当前 leader 数：

- `leaderCount(node) >= max` -> Unschedulable
- 否则通过

适合：

- 希望调度时强限制
- 可接受自定义 scheduler 维护成本

补强建议：

- 配合 `Reserve/Unreserve` 处理并发调度竞争

---

### 路线 B：Operator + Node Label + nodeAffinity（维护成本低）

Operator 周期性或事件驱动：

1. 查询业务 API 得到真实 leader
2. 映射 leader -> pod -> node
3. 统计每个 node leader 数
4. 给“已满节点”打 label（如 `leader-full=true`）

Pod 调度时使用 nodeAffinity 避开：

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: jraft.example.com/leader-full
          operator: DoesNotExist
```

适合：

- 不想维护 scheduler 插件
- 接受最终一致（运行时冲突由 Operator 修正）

---

## 4. 推荐组合策略（会话结论）

动态 Leader 场景推荐：

```text
Operator 感知真实 leader
+ Scheduler 约束新/重建 Pod 的调度落点
+ Operator 运行时冲突修正（优先 leader transfer）
```

修正优先级：

1. leader transfer（首选，扰动最小）
2. 迁移/重建 follower
3. 最后才删除 leader Pod（风险高）

---

## 5. 示例：maxLeadersPerNode = 2

约束：

```text
forall node: leaderCount(node) <= 2
```

### 5.1 Filter Plugin 伪代码

```go
if !isLeaderPod(pod) {
  return Success
}

count := countLeaderPodsOnNode(node)
if count >= 2 {
  return Unschedulable("node has 2 leaders already")
}
return Success
```

### 5.2 Operator 打 Node Label 伪逻辑

```text
leaders = queryAllShardLeaders()
countByNode = aggregate(leaders)

for each node:
  if countByNode[node] >= 2:
    label node: jraft.example.com/leader-full=true
  else:
    remove label jraft.example.com/leader-full
```

---

## 6. 为什么“Pod 反亲和性”不适合表达 max=2

`podAntiAffinity.required...` 更自然表达：

- “不能与某类 Pod 同节点” -> 接近 max=1

而 `max=2` 是“计数上限”语义，原生 anti-affinity 不擅长直接表达。

`topologySpreadConstraints` 可做均衡，但不总是等价于绝对上限。

---

## 7. 可观测性与告警建议

### 7.1 查看 leader 分布

```bash
kubectl get pod -A -l jraft.example.com/role=leader -o wide
```

### 7.2 查看 Node 是否被标记满载

```bash
kubectl get nodes -L jraft.example.com/leader-full
```

### 7.3 调度失败信号

```bash
kubectl describe pod <pod> -n <ns>
```

常见：

- `FailedScheduling`
- `node(s) didn't match Pod's node affinity/selector`
- 插件自定义拒绝原因

### 7.4 建议指标

- `jraft_leader_count_by_node`
- `jraft_leader_placement_violations_total`
- `jraft_leader_transfer_attempts_total`
- `jraft_leader_transfer_success_total`

---

## 8. 风险与边界条件

1. **物理不可满足**：leader 总数 > 可用 node 容量上限（`nodes * 2`）
2. **并发窗口**：仅 nodeAffinity 可能出现短暂超限（需 Operator 回收）
3. **存储拓扑约束**：PVC/PV 可能限制 Pod 可迁移范围
4. **业务可用性约束**：leader 迁移频率过高可能影响写延迟

---

## 9. 最小可行实施计划（MVP）

1. 给所有 shard Pod 增加稳定标签（app/shard/ordinal）
2. 实现一个只读探测器：周期查询 leader 并输出分布
3. 实现 Operator patch Pod role label（leader/follower）
4. 实现 Node label（leader-full）与 nodeAffinity 规避
5. 引入 leader transfer 自动修正
6. 再评估是否需要 Scheduler Plugin（强一致需求时）

