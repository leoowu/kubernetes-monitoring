# Stage 3 · Agent + Harness：角色、审批门、工作流闭环

> 上承 Stage 2：RAG = 组织记忆；MCP = 工具总线（你方诊断机器人目前 L1 只读）。  
> 本 Stage：把「会查」升级为「按组织角色与门禁可行动」——对齐轴 D。

## 框架对齐

| 概念 | 含义 |
|------|------|
| Agent | 带目标、可多步规划、会调工具的执行单元（不是单次 Chat） |
| Harness | 套在 Agent 外的约束与编排：角色、状态机、审批、审计、重试、停止条件 |
| 轴 D | 组织与体系：人机协作、SOP、人工门禁 —— 独立轨，不是应用附属 |

一句话：**Agent 负责办事；Harness 负责不让它乱办事。**

---

## 1. 为什么 Stage 2 不够

只读诊断可以停在 Stage 2。一旦出现：

- 改探针 / 重启 / 扩缩容 / 回滚  
- 对外发声（工单公众回复）  
- 写知识库「正式发布」  

就必须有 **角色 × 权限 × 审批 × 审计**。否则工具一放开，四类幻觉里的越权与工具幻觉会直接变成事故。

---

## 2. Harness 最小结构

```text
触发（告警 / 用户提问 / 工单）
  → 路由到角色化 Agent（Triage / Runbook / Change…）
  → 状态机：plan → act(read) → propose(write) → approve → act(write) → verify → close
  → 每步：策略引擎（角色、环境、工具等级）+ 审计
  → 停止条件：成功 / 拒绝 / 超时升级 / 人工接管
```

Harness 必有能力：

1. **角色绑定**：哪个 Agent 能看什么知识域、能调什么工具级  
2. **工具分级门**：L0/L1 可自动；L2+ 必须审批  
3. **人工门禁**：批准 / 驳回 / 改参后再批  
4. **审计与回放**：prompt、工具 trace、谁点了批准  
5. **升级与超时**：审批人超时 → 下一级 Oncall  

---

## 3. 角色化 Agent（对接侧轨 O）

| 角色 | 目标 | 默认可用工具 | 门禁 |
|------|------|--------------|------|
| Triage Agent | 归类、捞证据、列假设 | L0/L1 只读 MCP | 高危话术拦截 |
| Runbook Agent | 匹配 SOP、生成检查清单 | RAG + L1 | 不写生产 |
| Change Agent | 起草变更与回滚 | 读 + 写草案到运维平台 | **执行前必批** |
| Knowledge Curator | 复盘入库 | 写知识库草稿 | 正式发布必批 |
| Human Oncall | 最终责任 | 全部（经平台） | — |

同一条诊断会话里，可以是「一个大脑多角色提示」，也可以是「多 Agent 接力」；Harness 管的是 **权限与状态**，不绑死实现。

---

## 4. 与你当前机器人的接法

现状：MCP = EKS / Grafana / Loki / AWS / 运维平台，**只读**。  

Stage 3 不先狂开写权限，而是：

```text
Stage 2 诊断闭环（已有）
  → 输出「变更草案」（目标、风险、回滚、证据链接）
  → 进入 Harness 审批态
  → 人批通过后
  → 才短暂启用 L2 写工具（或人在运维平台点执行）
  → verify：再用 L1 只读确认 Ready/指标恢复
  → close + 审计包
```

两种落地强度：

| 模式 | 写法 | 适用 |
|------|------|------|
| A. 人执行 | Agent 只写变更单；人在平台点按钮 | 起步最安全 |
| B. Agent 执行 | 批准后 Harness 调 L2 MCP | 门禁与回滚成熟后 |

---

## 5. 状态机示例（诊断 → 变更）

```text
IDLE
  → DIAGNOSING      （Triage+Runbook，L1 MCP）
  → DIAGNOSIS_READY （结论+证据）
  → CHANGE_DRAFTED  （Change Agent 出草案）
  → PENDING_APPROVAL
       ├─ rejected → DIAGNOSIS_READY 或 CLOSE
       └─ approved → APPLYING（L2 或人执行）
            → VERIFYING（L1 复查）
                 ├─ recovered → CLOSED
                 └─ failed → ROLLBACK_PROPOSED → 再审批
```

审批单最小字段：环境、对象、动作、依据（tool/doc id）、风险、回滚、窗口、申请人/Agent id。

---

## 6. 幻觉在 Stage 3 的落点

| 幻觉 | Harness 侧闸 |
|------|----------------|
| 事实幻觉 | 变更单强制挂证据；无证据不可进 PENDING_APPROVAL |
| 指令漂移 | 状态机拒绝跳步（不能从 DIAGNOSING 直接 APPLYING） |
| 工具幻觉 | 无成功 tool trace 不得写「已执行」；APPLYING 必须有执行 id |
| 越权幻觉 | 角色×工具矩阵；未批准禁止 L2；跨租户直接拒 |

---

## 7. 心智模型

**Stage 2 解决「感知」；Stage 3 解决「组织化行动」。**  
Agent 是执行者，Harness 是变更管理系统在 AI 上的投影：角色、门禁、状态机、审计、升级。
