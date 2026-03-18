---
name: pkm-refactor
description: 个人知识库（PKM）重构与笔记分流。当用户提到"整理笔记"、"清理 Inbox/Other"、"笔记库乱了"、"分流笔记"、"知识库整理"、"整理 other.md"、"PKM 重构"时，必须使用此 skill。将碎片化的收件箱笔记按领域（技术、职业、生活、读书、健康、任务）提取并分发到结构化目录，同时保证 Front Matter、术语、文件命名、双向链接等规范一致性。
---

# pkm-refactor

此技能提供了一套标准化的工作流，用于将"碎片信息收集桶"转化为结构化的个人知识体系。

## 核心分流工作流

### 1. 扫描与分类 (Scan & Classify)
首先全面阅读目标文件（通常是 `other.md` 或 `Inbox.md`），将内容块划分为以下领域：

| 领域 | 关键字/特征 | 目标目录/文件 |
| :--- | :--- | :--- |
| **技术沉淀 (Skills)** | Bug 修复记录、技术原理总结、代码片段、架构图 | `Skills/2026` |
| **读书/文章笔记 (Reading)** | 读书心得、公众号文章总结、播客摘要 | `ReadNote/2026` |
| **职业/面试 (Career)** | 岗位 JD、面试复盘、简历修改建议、行业调研 | `Interview/2026` |
| **个人生活 (Life)** | 财务记录、通勤规划、社交记录、购物清单 | `Life/2026` |
| **健康管理 (Health)** | 疾病预防、体检建议、运动习惯 | `Health/2026` |
| **待办/项目灵感 (Tasks)** | 任务清单、未来项目想法、学习计划 | `other.md` (作为收件箱保留) |

### 2. 精炼与提取 (Refine & Extract)
- **去噪**：剔除无意义的临时记录或已完成的琐事。
- **结构化**：为提取出的技术点或笔记添加清晰的 Markdown 标题、列表和表格。
- **关联性**：如果新笔记与现有文档相关，应考虑合并或交叉引用。

### 3. 分发与重组 (Distribute & Refactor)
- **写入新文件**：为重要的主题创建独立的 `.md` 文件。
- **追加现有文件**：将零碎的生活记录或健康贴士追加到 `personal_life.md` 或 `health/` 目录下的汇总文件中，遵循聚合文件结构规范（见下文）。

### 4. 优化收件箱 (Reset Inbox)
- 清空原始文件，仅保留 **待办任务** 和 **未来灵感**。
- 为原始文件添加"分流说明"或"上一次清理日期"。

---

## 笔记文件标准模板

每个新建的独立 `.md` 文件必须以以下 YAML Front Matter 开头：

```yaml
---
title: {{标题}}
description: {{一句话说清这篇笔记的核心价值，面向 AI 检索优化}}
tags: [{{领域}}, {{关键词1}}, {{关键词2}}]
date: {{YYYY-MM-DD}}
source: {{来源：实践总结 / 书名 / 文章URL}}
status: draft             # draft | stable | needs-review
last_verified: {{YYYY-MM-DD}}   # 上次确认内容仍然有效的日期，初次创建与 date 相同
confidence: medium        # high | medium | low
related: []               # [[关联文件名]]，新建后需在对方文件中反向补充
---
```

### `description` 字段写作规范

- 一句话，不超过 50 字
- 直接说明"这篇笔记能解决什么问题"或"核心结论是什么"
- 使用与正文、glossary.md 一致的术语，严禁同义词混用
- 不要写"本文介绍了…"这类空洞开头，直接陈述结论

示例：
```yaml
description: 通过 proxy_pass 指令将 HTTP 请求转发到上游服务，适用于隐藏后端端口和统一入口的场景。
```

### `status` 与 `last_verified` 联动规则

| status | 含义 | last_verified 要求 |
| :--- | :--- | :--- |
| `draft` | 内容未完善，不可直接引用 | 可暂不填写 |
| `stable` | 内容经过验证，可直接引用 | 必填，每次复查后更新 |
| `needs-review` | 内容可能已过时，需人工确认 | 保留上次验证日期 |

> 技术类笔记建议每 6 个月将 `stable` 主动降级为 `needs-review`，重新验证后再升回。

### `confidence` 字段说明

- `high`：内容已在生产环境验证，可直接复用
- `medium`：内容经过测试但场景有限，引用时需结合实际
- `low`：当时的猜测或未经验证的想法，AI 引用时应保守对待

### `related` 双向维护规范

`related` 字段建立的是双向链接。新建笔记 A 引用了笔记 B 后，**必须同时打开笔记 B，在其 `related` 中补充 `[[A]]`**。单向链接会导致 AI 从 B 出发时无法发现 A 的存在。

---

## 笔记正文结构规范

Front Matter 之后，正文按以下顺序组织（根据领域可裁剪）：

```markdown
## 背景 / 问题
（为什么需要这篇笔记，遇到了什么问题）

## 原理 / 方案
（核心内容，技术类包含代码片段）

## 实践记录
（实际操作步骤、踩坑记录）

## 我的反思
（个人理解、延伸思考）

## 相关笔记
- [[关联文件名]]
```

### 自包含首句规范

每个 `##` 段落的**第一句话**必须能脱离上下文独立成立，方便 AI RAG 检索时单独引用该段落。

**坏的首句（依赖上下文）：**
```markdown
## 实践记录
按照上面的步骤操作后，需要重启服务才能生效。
```

**好的首句（自包含）：**
```markdown
## 实践记录
修改 Nginx 配置文件后，必须执行 `nginx -s reload` 才能使新配置生效。
```

---

## 聚合文件结构规范

`personal_life.md`、`health/` 下的汇总文件等多条追加写入的聚合文件，内部使用**日期 + 小标题**的条目结构，每条记录首句自包含：

```markdown
### 2026-03-18 · 体检建议
每年体检应包含空腹血糖和血脂四项，35岁以上建议加做颈动脉超声。
具体内容...

---

### 2026-01-10 · 健身计划调整
将每周跑步从3次调整为2次+1次力量训练，原因是膝盖有轻微不适。
具体内容...
```

最新记录放在文件**顶部**，便于 AI 优先读取最新内容。

---

## 笔记命名规范

- 技术/读书笔记：`主题名称.md`，如 `Nginx_Reverse_Proxy_Setup.md`
- 岗位调研：`公司名_岗位参考.md`
- 关键词优先英文，中英文结合（提升 AI 文件名检索准确率）
- 文件名即关键词，禁止使用 `note1.md`、`temp.md` 等无意义命名

---

## 术语一致性规范

**同一概念在所有笔记中只使用一个术语**，覆盖四个位置：文件名、`tags`/`description`、正文标题、正文内容，四处必须统一。

常见易混淆对照表（每组只选一个，全库统一）：

| 概念 | 选定术语 | 禁止混用 |
| :--- | :--- | :--- |
| 异步任务队列 | 消息队列 | MQ、任务队列、队列 |
| 容器编排 | Kubernetes | K8s（仅缩写时可用） |
| 持续集成 | CI/CD | 流水线、pipeline |

在 `Skills/glossary.md` 中维护完整术语表。**新建笔记前先查阅 glossary.md**，遇到不确定的术语先写入术语表再开始写笔记。

---

## 目录深度规范

目录层级**最深两层**，靠文件名和 `tags` 区分细分领域，不靠目录层级。

**正确：**
```
Skills/
  Nginx_Reverse_Proxy_Setup.md     # tags: [nginx, 运维, 网络]
  asyncio_Queue_Best_Practices.md  # tags: [python, 异步, 消息队列]
```

**错误：**
```
Skills/
  backend/
    network/
      Nginx_Reverse_Proxy_Setup.md
```

目录层级过深会在 AI 列举文件时消耗大量上下文窗口，且对人类搜索也无额外帮助。

---

## 示例操作

如果你发现 `other.md` 中有一段关于"如何配置 Nginx 反向代理"的记录，应当：

1. 提取并润色内容，查阅 `Skills/glossary.md` 确认术语
2. 创建 `Skills/2026/Nginx_Reverse_Proxy_Setup.md`，写入完整 Front Matter：
   ```yaml
   ---
   title: Nginx 反向代理配置
   description: 通过 proxy_pass 指令将请求转发到上游服务，适用于隐藏后端端口、统一入口等场景。
   tags: [nginx, 运维, 网络]
   date: 2026-03-18
   source: 实践总结
   status: stable
   last_verified: 2026-03-18
   confidence: high
   related: [[Docker_Network_Setup]]
   ---
   ```
3. 打开 `Docker_Network_Setup.md`，在其 `related` 中反向补充 `[[Nginx_Reverse_Proxy_Setup]]`
4. 从 `other.md` 中删除该段落
5. 在 `other.md` 顶部更新分流说明：
   ```markdown
   <!-- 上次清理：2026-03-18 | 已分流：Skills/2026/Nginx_Reverse_Proxy_Setup.md -->
   ```