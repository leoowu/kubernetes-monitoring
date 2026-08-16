# AI-Ops 学习库（长期维护版）

面向「资深运维 + 多模型重度用户」的 AI 原生组织/平台能力建设路径。  
本目录按 `00-background` / `01-learning-framework` 约束持续追加，与仓库内 `docs/k8s-study/` 并列维护。

## 文档结构

| 文档 | 用途 |
|------|------|
| [00-background.md](./00-background.md) | 学习者背景档案（持续追加） |
| [01-learning-framework.md](./01-learning-framework.md) | 四轴 + 七阶段总框架（v0.2） |
| [02-stage0-coordinate-system.md](./02-stage0-coordinate-system.md) | Stage 0：坐标系（北极星 / OSI / 六层 / 四轴） |
| [03-stage1-physics-interface.md](./03-stage1-physics-interface.md) | Stage 1：物理与接口（Token / API / 幻觉边界） |
| [experiments/E1-multimodel-control.md](./experiments/E1-multimodel-control.md) | Episode 1 实验：四模型对照 |
| [side-tracks/P-private-deploy.md](./side-tracks/P-private-deploy.md) | 侧轨 P：私有化推理起步 |
| [side-tracks/O-org-spec.md](./side-tracks/O-org-spec.md) | 侧轨 O：虚拟小团队规格（SDD） |
| [PROGRESS.md](./PROGRESS.md) | 进度与下一动作 |

## 当前焦点（2026-08-16）

- **已完成归档**：背景档案 v0.2、学习框架 v0.2
- **本轮推进**：Stage 0 坐标系固化 + Stage 1 Episode 1（机制课 + 四模型对照实验设计 + 私有化引子）
- **侧轨启动**：P 轨从 Stage 1 末开始；O 轨先写规格，Stage 3 再可执行化

## 维护模板（每次追加）

1. 概念定义（机制优先）
2. 控制流 + 数据流
3. 与运维职责的交汇点（SLO / 成本 / 沙箱 / 可观测）
4. 最小可做实验 / 观测命令
5. 常见失败模式与定位
6. 设计权衡（多模型 / 私有化 / 组织流程）

## 深度默认

- 轴 A / C / D：目标 L2–L3
- 轴 B：默认 L2，Transformer 关键路径可到 L3
- 不做研究级 L4
