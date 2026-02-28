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

## 🤝 贡献新 Skill

1. 在 `skills/` 下创建以 skill 名称命名的目录
2. 编写 `SKILL.md`，需包含 YAML frontmatter（`name`、`description`）和使用说明
3. 如有脚本，放在 `scripts/` 子目录下
4. 更新本 README 的 Skills 列表
