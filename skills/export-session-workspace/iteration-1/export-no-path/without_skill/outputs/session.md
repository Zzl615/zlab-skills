# 会话导出 — Node.js 项目 CI 配置

**导出时间:** 2026-04-16  
**主题:** 为 Node.js 项目配置 GitHub Actions CI 流水线

---

## Round 1 — 需求确认

**用户:**
> 帮我给这个 Node 项目加个 CI，要跑测试

**Claude:**
> 好的，我需要了解几个信息：
> - Node.js 版本是多少？
> - 测试命令是什么（比如 `npm test` 或 `yarn test`）？
> - 是否需要缓存 node_modules 以加速构建？

**用户:**
> Node 18，npm test，要缓存

---

## Round 2 — 创建 CI 配置文件

**Claude:**

根据你的要求，我创建了 `.github/workflows/ci.yml`，内容如下：

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test
```

> 文件已写入 `.github/workflows/ci.yml`。

**用户:**
> 能加上 lint 吗

---

## Round 3 — 添加 Lint 步骤

**Claude:**

好的，我在测试步骤之前加上了 `npm run lint`，更新后的 `.github/workflows/ci.yml` 如下：

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run lint
        run: npm run lint

      - name: Run tests
        run: npm test
```

> Lint 步骤已添加在测试之前，确保代码质量检查先于测试执行。

**用户:**
> 好的，看起来不错

---

## 最终产出

**文件:** `.github/workflows/ci.yml`

**配置摘要:**
- Node.js 版本: `18`
- 包管理器缓存: `npm`
- 步骤顺序: checkout → setup Node → install → lint → test
- 触发条件: push 或 PR 到 `main` 分支
