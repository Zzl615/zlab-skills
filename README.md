# zlab-skills

A curated collection of reusable AI-agent skills for software engineering workflows, including git analysis, commit generation, code review automation, and structured task execution.

## 📦 Skills 列表

| Skill | 触发词 | 功能描述 |
| --- | --- | --- |
| [git-smart-commit](skills/git-smart-commit/SKILL.md) | `gsc`、"分析提交" | 分析 git 变更，按功能拆分并生成 Angular 规范的中文 commit 信息 |
| [tapd-xls-to-md](skills/tapd-xls-to-md/SKILL.md) | 文件名以 `_tapd.xls` 结尾 | 将 TAPD 导出的损坏/二进制 XLS 文件转换为 Markdown Bug 列表或详细报告 |
| [code-to-stories](skills/code-to-stories/SKILL.md) | "代码转用户故事" 等 | 从代码中逆向提取业务逻辑，自动生成 User Story 和 Gherkin 验收场景 |

## 🚀 安装与使用

### 方式一：符号链接（推荐）

将本仓库的 `skills` 目录链接到 Antigravity 的 skills 配置路径：

```bash
# 备份已有 skills（如果有）
mv ~/.gemini/antigravity/skills ~/.gemini/antigravity/skills.bak

# 创建符号链接
ln -s /path/to/zlab-skills/skills ~/.gemini/antigravity/skills
```

### 方式二：手动复制

将需要的 skill 目录复制到 Antigravity 的 skills 路径下：

```bash
cp -r skills/git-smart-commit ~/.gemini/antigravity/skills/
cp -r skills/tapd-xls-to-md ~/.gemini/antigravity/skills/
cp -r skills/code-to-stories ~/.gemini/antigravity/skills/
```

---

## 📖 Skill 详细说明

### 🔀 git-smart-commit (gsc)

分析当前 git 变更，自动按功能维度拆分并生成符合 [Angular Commit 规范](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit) 的中文提交信息。

**触发方式：** 输入 `gsc` 或提及"分析提交"

**工作流程：**

1. **深度扫描** — 运行 `git diff --cached`（无暂存文件时扫描工作区）
2. **功能解构** — 按功能（而非文件）维度拆分变更
3. **生成规范** — 为每个功能生成 `<type>(<scope>): <subject>` 格式的中文 commit
4. **呈现方式** — 列出提交序号、提交信息及涵盖的文件
5. **待命确认** — 询问是否执行提交

**支持的 Type：** `feat` | `fix` | `docs` | `style` | `refactor` | `test` | `chore`

---

### 📊 tapd-xls-to-md

将 TAPD 导出的 XLS 文件（BIFF8 格式）转换为 Markdown 文档。适用于标准库（如 `pandas`、`xlrd`）无法读取的损坏文件。

**触发条件：** 文件名以 `_tapd.xls` 结尾，或标准 Excel 读取工具报错

**两种输出模式：**

#### 📋 简洁列表模式

生成格式为 `序号: 标题 ID 【标题】 URL` 的 Bug 清单：

```bash
python3 <skill_dir>/tapd-xls-to-md/scripts/xls_to_md.py <path_to_xls_file> > bug_list.md
```

#### 📝 详细报告模式

生成按迭代分组的详细 Bug 报告（含标题、描述、评论）：

```bash
python3 <skill_dir>/tapd-xls-to-md/scripts/xls_to_detail.py <path_to_xls_file> > bug_detail.md
```

**依赖：** Python 3（仅使用标准库 `sys`、`struct`、`re`，无需安装额外包）

---

### 📖 code-to-stories

将任意代码逆向转化为标准 User Story 和可直接使用的 Gherkin `.feature` 文件。适用于从代码生成需求、补齐遗留系统文档等场景。

**触发条件：** 提及"从代码生成需求"、"代码转用户故事"、"生成 gherkin"、"分析这段代码的业务逻辑"等。

**主要功能：**

1. **代码分析** — 识别代码边界、模式、角色（Actor）并建立场景矩阵。
2. **生成 User Story** — 基于识别出的业务流，生成符合 INVEST 原则的标准 User Story。
3. **生成 Gherkin 特性文件** — 提供完整的 `Given`/`When`/`Then` 测试用例（涵盖正向、异常和边界条件）。
4. **结构化完整输出** — 提供统一规范的 Markdown 输出，包含业务逻辑分析、场景矩阵、US、Gherkin 及局限性说明。

---

## 📁 目录结构

```
zlab-skills/
├── README.md
├── LICENSE
└── skills/
    ├── code-to-stories/
    │   └── SKILL.md
    ├── git-smart-commit/
    │   └── SKILL.md
    └── tapd-xls-to-md/
        ├── SKILL.md
        └── scripts/
            ├── xls_to_md.py
            └── xls_to_detail.py
```

## 📝 Skill 开发规范 (基于 Anthropic Guidelines)

如果你想贡献新的 Skill，请遵循以下规范：

### 1. 结构与文件
- 在 `skills/` 下创建以 skill 名称命名的目录。
- 必须包含 `SKILL.md` 文件。
- 如果有可执行脚本、庞大的 Prompt Context，建议按职责存放到 `scripts/`、`references/` 等子目录，实现**渐进式披露 (Progressive Disclosure)**（即按需加载，避免污染主提示词空间）。
- 建议提供测试验证用例并存放于 `evals/evals.json` 中。

### 2. 编写 SKILL.md
- **Frontmatter 必须完整**：文件顶部必须包含 YAML 语法的 `name` 和 `description`。
- **Trigger 词写在 Description 里**："When to use"（什么时候该触发该 skill）的描述**必须且只能**写在 `description` 中。不要在 markdown 正文中单开一节写 "When to use"。
- **Description 要有引导性（Pushy）**：为了防止 Agent "漏触发"（undertrigger），`description` 应该具有强烈的引导性。例如："当用户提及 XXX 时，即使只说了 YYY，也**必须**使用本 skill"。
- **字数限制**：`SKILL.md` 的正文部分尽量控制在 500 行以内。如果有超长的参考文件（>300行），请放到 `references/` 里并包含目录。
- **使用祈使句**：在核心指令中，多使用明确的祈使句告知 Agent 该做什么。
- **提供示例 (Examples pattern)**：给出具体的 Input 和 Output 范例，或者格式模板。

### 3. 提交流程
1. 完成 `SKILL.md` 编写后，在项目中更新主 `README.md` 的 Skills 列表。
2. 添加相应的说明和用例。
