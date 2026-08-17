# 验证证据

这里记录 S0–S7 的可复现验证结果，不存整个 `midnightroad/build/`，也不把 DEV 模拟证据冒充微信真机证据。

每刀使用 `S0.md` 到 `S7.md`。S0 当前记录在 [S0.md](S0.md)。证据 ID 格式：

```text
S<n>-CORE-<nn>
S<n>-CREATOR-<nn>
S<n>-PKG-<nn>
S<n>-DEVTOOLS-<nn>
S<n>-DEVICE-<nn>
```

## 记录模板

```markdown
## <Evidence ID> · <简短名称>

- Result: PASS | FAIL | BLOCKED
- Timestamp: YYYY-MM-DD HH:mm Asia/Shanghai
- Contract commit: <sha>
- Cocos branch / base / result: <branch> / <sha> / <sha>
- Environment: <Creator、开发者工具、微信、设备、基础库、MCP 版本>
- Preconditions: <seed、车辆、profile、网络、AppID 类型；不写敏感值>
- Steps: <可重放步骤>
- Expected: <可测结果>
- Actual: <实际结果或原始错误>
- Artifact: <相对路径或稳定本机路径 + 内容哈希>
- Limits: <模拟能力、未测分支、唯一下一步>
```

FAIL 证据不删除；修复后新增 ID 并链接旧记录。微信小游戏助手浏览器预览归 `PKG`，开发者工具归 `DEVTOOLS`，真实微信手机归 `DEVICE`。完整规则见 [完整开发方案](../plan.md) §9。
