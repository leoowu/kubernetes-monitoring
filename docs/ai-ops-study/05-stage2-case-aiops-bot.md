# Stage 2 案例：AI 运维机器人（查询 / 诊断 / 分析）

> 场景：问题查询与诊断分析  
> 工具面（MCP，当前均为只读）：EKS · Grafana · Loki · AWS · 运维平台  
> 对齐：RAG = 组织知识库；MCP = 工具总线

## 1. 角色边界

| 部件 | 职责 | 不负责 |
|------|------|--------|
| 模型 | 理解问题、选工具、综合证据、给出假设与下一步 | 不直接改集群；不「假装已查询」 |
| RAG 知识库 | 提供 SOP、服务地图、历史复盘、告警释义 | 不提供此刻集群真实状态 |
| MCP 工具总线 | 受控只读探测（EKS/Grafana/Loki/AWS/运维平台） | 当前不开放 apply/重启/删资源 |

当前策略：**整条诊断链路停在 L1（只读生产查询）**，写变更留给 Stage 3 审批门。

## 2. 一次诊断的端到端流

```text
用户：「prod-payments 里 payments-api Ready 为 False，帮我查」
  │
  ├─① 会话与权限
  │    身份 → 租户/环境范围（只能碰 prod-payments 相关只读接口）
  │
  ├─② RAG（组织记忆）
  │    检索：payments-api Runbook、依赖图、历史同类复盘、探针规范
  │    注入：带 doc_id 的摘录 +「无工具证据勿断言现状」
  │
  ├─③ 模型规划（仍在窗口内）
  │    假设候选 → 决定调用哪些只读工具、什么顺序
  │
  ├─④ MCP 工具总线（只读执行）
  │    EKS:     get/describe pod/deploy/events；日志尾部（若经授权）
  │    Grafana: 查仪表盘/瞬时指标（CPU、饱和度、错误率）
  │    Loki:    按 label/时间窗拉错误日志
  │    AWS:     只读（如 ALB 5xx、RDS 连接、限流相关 Describe*）
  │    运维平台: 变更窗、近期工单、服务负责人、CMDB 依赖
  │    ↑ 每步：鉴权 → 参数校验 → 超时 → 审计 → 结果回写 messages
  │
  ├─⑤ 模型综合
  │    现象 / 证据表 / 分层假设 / 建议的下一条只读动作
  │    引用：知识库 doc_id + 工具调用 id
  │
  └─⑥ 停止线
       需要重启/改探针/扩容 → 只输出「变更草案」，不调用写工具（Stage 3）
```

## 3. 知识库（RAG）在本场景装什么

| 知识域 | 内容例 | 检索何时用 |
|--------|--------|------------|
| Runbook | Ready=False 标准检查单 | 问题一进来 |
| 服务目录 | payments-api 依赖：DB、Redis、下游 | 解释「该查谁」 |
| 告警词典 | 探针 timeout / throttle 含义 | 对齐术语 |
| 复盘 | 近 90 天同类事故 | 先验假设排序 |
| 禁区说明 | 哪些日志字段脱敏、哪些命名空间不可见 | 与 ACL 双保险 |

原则：**RAG 回答「我们通常怎么看」；MCP 回答「现在机器上是什么」。**

## 4. MCP 工具地图（只读）

| 服务器 | 典型只读能力 | 诊断中的用途 |
|--------|--------------|--------------|
| EKS | get/describe/list pod、deploy、events、node；只读 logs | 确认 Ready、Events、重启、调度 |
| Grafana | 查询面板/Prometheus 瞬时或区间指标 | CPU throttle、饱和、错误率 |
| Loki | LogQL 只读查询 | 应用报错、依赖超时栈 |
| AWS | 只读 Describe/Get（ELB、RDS、SQS…按最小权限） | 区分「应用内」vs「云产品侧」 |
| 运维平台 | 工单、值班表、CMDB、变更记录只读 | 负责人、近期是否在变更窗 |

总线必须做的事（每次调用）：

1. 身份与环境范围校验（禁止跨租户）  
2. 动词白名单（仅 get/describe/query；拒绝 apply/delete）  
3. 超时与结果大小上限（防日志把窗口打爆）  
4. 审计：谁、何时、哪个 tool、参数摘要、结果摘要  

## 5. 例子：Ready=False（把 Stage 1+2 串起来）

**用户输入：** `payments-api-… Ready False，Events 里 readiness timeout`

**RAG 命中：** Runbook「探针失败优先看应用阻塞/依赖/CPU/探针过严」

**模型规划的工具序（示例）：**

1. EKS `describe pod` → 确认 State=Running、Ready=False、Events  
2. EKS / Loki → 应用日志是否大量依赖超时  
3. Grafana → 容器 CPU throttle、下游延迟  
4. AWS → 若怀疑 ALB/RDS，只读查目标组健康与 DB 连接  
5. 运维平台 → 近 1h 是否有关联变更单  

**合格输出形态：**

- 现象：Running 但 Ready=False，readiness HTTP 超时  
- 证据：工具返回摘要（带调用 id）  
- 假设排序：应用 `/ready` 阻塞 > 依赖超时 > CPU 饥饿 > 探针 timeout 过短  
- 下一步：仍给**一条**只读建议；若建议改探针，标成「待审批变更」而非直接执行  

**不合格：** 未调工具却写「我查过 EKS」；或直接建议 `kubectl delete pod`。

## 6. 和 Stage 1 / Stage 3 的接口

- Stage 1：每次工具结果都占 token；要截断、摘要、分轮探测，否则窗口与费用爆掉  
- Stage 2（现在）：只读闭环已可上线值班辅助  
- Stage 3：把「变更草案」接角色、审批门、Harness，再开 L2 写工具  

## 7. 一句话

**AI 运维机器人 = 知识库里的组织经验 + MCP 只读总线里的现场证据 + 窗口内模型综合；当前停在诊断，不停在自动变更。**
