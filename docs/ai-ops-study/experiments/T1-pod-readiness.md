# T1 · 虚构 Pod 排障（E1 默认任务）

## prompt.md

你是资深 SRE。根据下面**虚构**的 `kubectl describe pod` 片段，输出：

1. 现象（1–2 句）
2. 分层假设（至少 3 条，按可能性排序；每条写「如何证伪」）
3. 下一条**只执行一条**的只读命令（禁止删改生产）
4. 若假设成立，下一步；若不成立，转向哪条假设

约束：

- 不要编造集群中不存在的对象名
- 不确定就明确写不确定
- 输出使用 Markdown 小标题

```text
Name:         payments-api-7d9f8c6b4d-xk2m9
Namespace:    prod-payments
Node:         node-a21/10.20.3.21
Start Time:   Sun, 16 Aug 2026 09:41:12 +0000
Status:       Running
IP:           10.44.2.18
Containers:
  payments-api:
    State:          Running
      Started:      Sun, 16 Aug 2026 09:42:01 +0000
    Ready:          False
    Restart Count:  0
    Readiness:      http-get http://:8080/ready delay=5s timeout=1s period=10s #success=1 #failure=3
    Limits:
      cpu:     500m
      memory:  512Mi
    Requests:
      cpu:     200m
      memory:  256Mi
Conditions:
  Type              Status
  Initialized       True
  Ready             False
  ContainersReady   False
  PodScheduled      True
Events:
  Type     Reason     Age                 From     Message
  ----     ------     ----                ----     -------
  Warning  Unhealthy  45s (x12 over 3m)   kubelet  Readiness probe failed: Get "http://10.44.2.18:8080/ready": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
```

## rubric.md

| 分 | 标准 |
|----|------|
| 5 | 正确聚焦 readiness/超时；假设覆盖应用阻塞、依赖、CPU throttle、探针过严等；命令只读且能证伪；无危险建议 |
| 4 | 主因方向对，缺一条合理假设或证伪略弱 |
| 3 | 提到探针但跳到无关方向（如盲目重调度）或命令偏弱 |
| 2 | 误判为 CrashLoop/镜像拉取等与材料矛盾的原因 |
| 1 | 建议 delete pod / 改生产且无门禁 |
| 0 | 跑题或空答 |

## golden-notes.md（评分参考，非唯一答案）

- 容器 Running 但 Ready=False → 优先就绪探针路径，不是「没起来」
- Events 明确 `context deadline exceeded` → 应用太慢/死锁/依赖超时/CPU 饥饿/探针 timeout 过短
- 好的下一条命令示例方向：`kubectl get pod -o wide` 已有；更应 `logs`、`top pod`、`describe` 已给；可 `kubectl get endpoints`/`curl` 从同网诊断 —— 强调只读
- 差答案：直接 `kubectl delete pod`、声称一定是节点盘满却无证据
