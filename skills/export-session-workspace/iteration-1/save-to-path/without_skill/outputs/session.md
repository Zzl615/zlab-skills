# Session Notes: FastAPI 500 错误调试

**Date:** 2026-04-16
**Topic:** FastAPI 服务返回 500 错误 — 数据库连接未初始化问题排查与修复

---

## Round 1 — 问题描述与初步排查

**User:**
> 我的 FastAPI 服务一直返回 500，日志里没看到什么有用的信息

**Claude:**
建议启用 debug 模式并更仔细地检查 uvicorn 日志：

```bash
uvicorn main:app --reload --log-level debug
```

**输出结果（关键错误）：**
```
AttributeError: 'NoneType' object has no attribute 'execute'
```
错误位置：数据库连接处理器（database connection handler）

---

## Round 2 — 定位根因

**User:**
> 找到了，是数据库连接没初始化

**Claude:**
确认根因：`db` 变量在测试模式下运行时，`startup` 事件尚未触发，导致 `db` 为 `None` 时就被使用。

**修复方案：** 在查询函数顶部添加 null 检查 + 懒加载初始化模式，修改 `database.py`：

```python
# database.py (临时修复)
def query(...):
    if db is None:
        db = create_engine(DATABASE_URL)
    ...
```

---

## Round 3 — 发现新问题并最终重构

**User:**
> 改了之后好了，但是现在每次请求都会重新创建连接

**Claude:**
解释这是连接池反模式（connection pool anti-pattern）。每次请求重新创建引擎会绕过连接池，导致性能下降和连接泄漏风险。

**最终重构方案：** 使用模块级单例（module-level singleton）配合 FastAPI 生命周期钩子：

```python
# database.py (最终版本)
engine = None

@app.on_event("startup")
async def startup():
    global engine
    engine = create_engine(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    engine.dispose()
```

**效果：** 连接引擎只在应用启动时创建一次，所有请求共享连接池，应用关闭时正确释放资源。

---

## 总结

| 阶段 | 问题 | 解决方案 |
|------|------|----------|
| 初步排查 | 500 错误无有效日志 | 启用 `--log-level debug` 暴露 `AttributeError` |
| 根因定位 | `db` 为 `None`，startup 未触发 | 懒加载 null 检查 |
| 深度优化 | 每次请求重建连接，绕过连接池 | 模块级单例 + lifecycle hooks |

**关键文件：** `database.py`
**最终状态：** 服务正常，连接池正确复用
