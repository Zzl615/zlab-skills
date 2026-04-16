# 为 Node.js 项目配置 GitHub Actions CI 流水线

# Timeline

## Round 1

### 用户

帮我给这个 Node 项目加个 CI，要跑测试

### AI

询问了三个关键信息：Node 版本是多少、测试命令是什么、是否需要依赖缓存。

### 执行

无

### 结果

用户回复：Node 18，npm test，要缓存。

---

## Round 2

### 用户

（确认了 Node 18、npm test、需要缓存后，AI 开始创建 CI 配置文件）

### AI

根据用户需求，创建了 `.github/workflows/ci.yml`，配置了：
- 触发条件：push 和 pull_request
- 运行环境：ubuntu-latest
- Node 版本：18
- npm 依赖缓存：启用
- 测试步骤：`npm test`

### 执行

使用 Write 工具创建文件 `.github/workflows/ci.yml`，内容如下：

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test
```

### 结果

文件写入成功。用户看到配置后问能否加上 lint。

---

## Round 3

### 用户

能加上 lint 吗

### AI

在 `npm test` 步骤之前插入了 `npm run lint` 步骤，保证代码风格检查先于测试执行，出错时反馈更明确。

### 执行

更新 `.github/workflows/ci.yml`，在 Run tests 步骤前添加 lint 步骤：

```yaml
      - name: Run lint
        run: npm run lint

      - name: Run tests
        run: npm test
```

### 结果

用户确认："好的，看起来不错"。CI 配置完成。

---

# Final Conclusion

## 问题本质

为一个 Node.js 项目从零配置 GitHub Actions CI 流水线，要求包含测试和代码检查。

## 关键结论

- 使用 `actions/setup-node@v4` 可以一步完成 Node 版本固定与 npm 缓存配置
- lint 步骤应放在 test 之前，确保代码质量问题优先暴露
- `npm ci` 比 `npm install` 更适合 CI 环境（严格锁版本、速度更快）

## 最终方案

在 `.github/workflows/ci.yml` 中配置以下流程：checkout → setup Node 18 + npm cache → npm ci → npm run lint → npm test。每次 push 和 PR 自动触发。

## 后续动作

- 确认项目 `package.json` 中已定义 `test` 和 `lint` 脚本
- 可按需添加其他触发条件（如仅在特定分支上触发）或矩阵测试（多 Node 版本）
