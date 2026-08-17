# ADR 0002：双仓与生成包治理

**Status**: accepted
**Date**: 2026-08-18

## Context

项目同时存在产品契约仓 `midnight-neon-racer/`、正式 Cocos 工程 `midnightroad/` 和 Creator 生成的 `midnightroad/build/wechatgame/`。旧 H5 也保留在契约仓归档。若后续 Agent 不区分这些边界，容易把验证代码当正式架构、手改生成包、把预览素材直接进包，或让聊天结论覆盖已确认需求。

## Decision

1. `midnight-neon-racer/` 是需求、ADR、开发方案、美术源、验收证据和恢复入口的权威仓。
2. `midnightroad/` 只负责 Cocos Creator 可运行源码、工程设置、测试与构建模板；它自己的 README/AGENTS 只解释实现边界，不复制产品规则。
3. `midnightroad/build/wechatgame/` 是可重建生成物，只供微信小游戏助手、开发者工具和真机验证；禁止直接实现或修补正式玩法。
4. 契约仓主动维护目录逐层使用 README 说明职责。Cocos `assets/` 受 Asset Database 管理，不放 README；其子目录职责集中记录在工程根 `docs/architecture.md`，序列化资产与 `.meta` 只由 Creator/Cocos MCP 管理。
5. 冻结归档、生成缓存、依赖、第三方扩展和工具状态目录不纳入 README 覆盖。

## Consequences

- 新会话先从契约仓 `PROJECT.md`、`CONTEXT.md`、`docs/new-session.md` 恢复，再进入 Cocos 工程。
- 产品规则变化必须先更新契约/ADR；实现进度和证据不能只留在聊天。
- Cocos 目录不会因为说明文件产生额外资源导入与 `.meta` 噪声，但维护者新增源码目录时必须同步工程 `docs/architecture.md`。
- 两个 Git 仓库分别建立可恢复基线；一个仓库的提交不能替代另一个仓库的状态记录。
