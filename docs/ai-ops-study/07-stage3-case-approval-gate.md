# Stage 3 案例：诊断机器人如何接上审批门

> 延续：AI 运维机器人；MCP 现况只读（EKS/Grafana/Loki/AWS/运维平台）

## 场景

诊断结论：`payments-api` Ready=False，证据指向 `/ready` 依赖 DB 超时；建议 **临时调高 readiness timeout** 并 **滚动重启**（示例，不代表真实最佳实践）。

## 无 Harness 时会发生什么（反例）

模型直接说：「我帮你改探针并重启了。」  
→ 越权幻觉 +（若未真调）工具幻觉；有写权限则会成真事故。

## 有 Harness 时的路径

1. **DIAGNOSING**：只读 MCP 取证（Stage 2）  
2. **CHANGE_DRAFTED**：Change Agent 生成变更单  
   - 对象：Deployment/Probe  
   - 依据：EKS events id、Loki 查询 id、Grafana 面板截取摘要  
   - 回滚：恢复原 timeout  
3. **PENDING_APPROVAL**：推给 Oncall；超时升级  
4. **批准后**  
   - 模式 A：人在运维平台执行  
   - 模式 B：Harness 调用 L2 写接口（需另开 MCP 写能力）  
5. **VERIFYING**：再用 EKS/Grafana/Loki 只读确认 Ready=True、错误率回落  
6. **CLOSED**：审计包归档；可选打给 Knowledge Curator 写复盘草稿

## 角色×工具矩阵（本场景）

| 角色 | EKS读 | Grafana/Loki/AWS读 | 运维平台读 | 改探针/重启 | 发公众回复 |
|------|-------|--------------------|------------|-------------|------------|
| Triage | ✓ | ✓ | ✓ | ✗ | ✗ |
| Change | ✓ | ✓ | ✓ | 批后✓ | ✗ |
| Human Oncall | ✓ | ✓ | ✓ | ✓ | ✓ |

## 审批单示例（字段）

```yaml
change_id: chg-20260816-0142
env: prod-payments
action: update_readiness_timeout + rolling_restart
target: deploy/payments-api
evidence:
  - tool: eks.describe_pod  id: call_01
  - tool: loki.query        id: call_04
risk: medium
rollback: restore probe timeout to 1s
requester: change-agent
approver: null  # pending
```
