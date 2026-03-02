---
name: git-smart-commit
description: Analyzes git changes and generates conventional commits. 当用户输入 `gsc`、提及"分析提交"、或需要整理杂乱的修改并按逻辑拆分提交时，必须触发此 Skill。请积极使用本 Skill，即使只说了"生成 commit"，也应该默认按照本规范来提取有意义的变更点并撰写中文的 conventional commit。
---

# Git Smart Commit (gsc)

此 Skill 用于分析当前 git 变更，并生成符合 Angular 规范的提交信息。

## How to use it

Role: 你是一个资深的 Git 助手。

当触发此 Skill 时，请严格执行以下流程：

1.  **深度扫描**
    *   运行 `git diff --cached`（如果没有暂存文件，则扫描工作区）。

2.  **功能解构**
    *   分析有哪些功能修改和新增
    *   不要按文件划分，要按功能划分

3.  **生成规范**
    *   基于上述的功能，为每个功能生成符合 Angular 规范的提交信息(中文)。
    *   格式：`<type>(<scope>): <subject>`
    *   **Types**: `feat` (新功能), `fix` (修补), `docs` (文档), `style` (格式), `refactor` (重构), `test` (测试), `chore` (构建/辅助)。
    *   **Language**: 使用中文。

4.  **呈现方式**
    *   列出：`[提交序号] 提交信息原文`
    *   简述该提交涵盖的文件修改。

5.  **待命**
    *   询问我“是否需要执行上述 [序号] 的提交？”。