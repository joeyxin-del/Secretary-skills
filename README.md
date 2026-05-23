# Secretary Skill（秘书技能）v2.0

全生命周期目标管理：从模糊愿景到归档复盘，一站式搞定。

帮助用户对抗长期目标的**三大杀手**：**Ambiguity（模糊）** — 不知从哪开始，**Overwhelm（压倒）** — 目标太大看着就做不动，**Oblivion（遗忘）** — 过几天就忘了。

## 5 阶段流水线

```
[一个模糊的想法]
       │
       ▼
 1. De-ambiguation    ──► 一次一问，锁定 Original Goal
       │
       ▼
 2. Vertical Splitting ──► 里程碑 → 2小时可执行原子任务
       │
       ▼
 3. Persistent Storage ──► 写入 ~/.hermes/goals/<slug>.md + memory
       │
       ▼
 4. Cron Automation   ──► 设置定时提醒 / 复盘任务
       │
       ▼
 5. Tracking & Review ──► 更新进度、追加复盘日志、状态流转
```

## 核心功能

| 功能 | 说明 |
|------|------|
| **去模糊化** | 一次问一个问题，像教练一样帮你把模糊想法变成清晰目标 |
| **垂直拆解** | 里程碑 → 子任务 → 2小时原子任务，深度可调 |
| **持久化存储** | 每个目标存为 `~/.hermes/goals/<slug>.md`，跨会话可检索 |
| **定时提醒** | 通过 Cron 设置每日/每周/每月复盘提醒 |
| **进度跟踪** | metrics 进度、复盘日志、状态流转（active/paused/completed/archived） |

## 协议命令

| 命令 | 阶段 | 说明 |
|------|------|------|
| `/init_goal [text]` | 1 | 启动去模糊引擎，一次一问 |
| `/split --depth [1-3]` | 2 | 拆解目标为里程碑 → 原子任务 |
| `/save` | 3 | 持久化当前目标到文件系统 |
| `/schedule --freq [daily/weekly/monthly]` | 4 | 创建 Cron 定时复盘 |
| `/align` | 5 | 计划偏离时重新校准 |
| `/status --report [slug]` | 5 | 查看目标进度 |
| `/goal list` | 5 | 列出所有已存储目标 |
| `/goal show <slug>` | 5 | 查看目标详情 |
| `/goal update <slug>` | 5 | 更新进度和复盘日志 |
| `/goal archive <slug>` | 5 | 归档已完成目标 |

## 数据存储格式

每个目标存为一个 Markdown 文件（YAML frontmatter + body）：

```yaml
---
title: "目标标题"
slug: my-goal
status: active        # active | paused | completed | archived
created_at: 2026-05-23
target_date: 2029-05-23
category: finance     # finance | health | career | learning | project
metrics:
  - name: 现金储蓄
    target: 1000000
    current: 0
    unit: 元
---
```

## 项目结构

```
SKILL.md          Secretary Skill 完整定义（Hermes Agent 加载入口）
README.md         本文件
src/              核心逻辑
commands/         CLI 命令实现
tests/            测试
references/       领域知识参考（如深圳社保公积金计算）
```

## 兼容性

- **Hermes Agent** — 原生支持（`hermes skills install secretary-skill`）
- **Claude Code** — 通过 `.claude/` 配置支持
- 协议设计可适配其他 AI Agent 框架

## 版本历史

- **v2.0.0** — 扩展为 5 阶段全生命周期：增加持久化存储和跟踪复盘
- **v1.0.0** — 初始版本：3 阶段流程（去模糊 → 拆分 → 定时）
