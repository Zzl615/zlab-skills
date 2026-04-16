# FastAPI 服务 500 错误排查与数据库连接修复

# Timeline

## Round 1

### 用户

我的 FastAPI 服务一直返回 500，日志里没看到什么有用的信息

### AI

建议开启 debug 模式并检查 uvicorn 的详细日志，以获取更多报错信息。

### 执行

```bash
uvicorn main:app --reload --log-level debug
```

### 结果

日志中出现关键报错：

```
AttributeError: 'NoneType' object has no attribute 'execute'
```

错误位于数据库连接处理器中，说明数据库连接对象为 `None`。

---

## Round 2

### 用户

找到了，是数据库连接没初始化

### AI

分析根本原因：`db` 变量在测试模式下运行时，`startup` 事件尚未触发就被使用，导致 `db` 为 `None`。建议添加空值检查和懒加载初始化模式，在查询函数顶部判断 `db` 是否已初始化。

### 执行

修改 `database.py`，在查询函数顶部添加懒加载判断：

```python
if db is None:
    db = create_engine(DATABASE_URL)
```

### 结果

修改后服务不再返回 500 错误，问题解决。

---

## Round 3

### 用户

改了之后好了，但是现在每次请求都会重新创建连接

### AI

解释这是连接池反模式（connection pool anti-pattern）：每次请求都调用 `create_engine()` 会导致连接无法复用，影响性能。正确做法是使用模块级单例，并配合 FastAPI 的生命周期钩子（startup/shutdown）进行初始化和清理。

### 执行

重构代码，使用 `@app.on_event` 管理数据库连接生命周期：

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = None
SessionLocal = None

@app.on_event("startup")
async def startup():
    global engine, SessionLocal
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.on_event("shutdown")
async def shutdown():
    global engine
    if engine:
        engine.dispose()
```

### 结果

连接池正确建立，每次请求复用已有连接，性能问题解决，生命周期管理符合 FastAPI 最佳实践。

---

# Final Conclusion

## 问题本质

FastAPI 服务在测试模式下数据库连接未初始化，导致请求时抛出 `AttributeError`，进而返回 500 错误。

## 关键结论

- 根本原因：`db` 变量在 `startup` 事件触发前被使用，值为 `None`
- 临时修复（懒加载）虽解决了 500 错误，但引入了每次请求重建连接的性能问题
- 正确方案：模块级单例 + FastAPI 生命周期钩子

## 最终方案

使用 `@app.on_event("startup")` 初始化 `create_engine()` 和 `SessionLocal`，使用 `@app.on_event("shutdown")` 调用 `engine.dispose()` 释放连接。数据库引擎作为模块级变量，整个应用生命周期内只初始化一次。

## 后续动作

- 考虑迁移到 FastAPI 新版推荐的 `lifespan` 上下文管理器（替代已废弃的 `on_event`）
- 对连接池参数（`pool_size`、`max_overflow`）进行调优以匹配生产负载
