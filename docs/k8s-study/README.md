# Kubernetes 学习文档索引（长期维护版）

本目录是从会话归档文档拆分出的结构化学习库，适合长期迭代维护。

## 文档结构

1. [01-mainline-lifecycle.md](./01-mainline-lifecycle.md)  
   主链路：从请求进入 API Server 到 Pod 创建、调度、运行、删除的完整生命周期。
2. [02-apiserver-admission-policy.md](./02-apiserver-admission-policy.md)  
   API Server 请求时检查：认证、鉴权、准入、默认化、校验，以及 ResourceQuota 等机制。
3. [03-observability-debug-playbook.md](./03-observability-debug-playbook.md)  
   可观测与排障手册：按阶段定位问题、常见症状与命令清单。
4. [04-jraft-leader-scheduling-strategy.md](./04-jraft-leader-scheduling-strategy.md)  
   JRaft Leader 分布约束专题：Scheduler Plugin 与 Operator 方案对比和落地建议。

## 与归档文档关系

- 完整会话归档：`/workspace/K8S_POD_LIFECYCLE_STUDY_ARCHIVE.md`
- 本目录是面向持续维护的专题化拆分版本。

## 建议维护方式

- 每次学习新增内容时，按以下模板补充到对应文档：
  1) 新概念定义  
  2) 控制流 + 数据流  
  3) 关键对象字段变化  
  4) 观测命令  
  5) 常见故障与定位  
  6) 设计权衡
