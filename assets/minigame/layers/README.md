# 赛道图层栈

720×1280 图层按 `00-sky` 到 `08-hud` 自下而上合成。规范读 `../../../docs/art/layers.md`；机器顺序和切换维度读 [stack.json](stack.json)；当前交付状态读 [manifest.md](manifest.md)。

每层目录的 README 说明职责，`manifest.md` 记录实际交付文件、尺寸、版本和缺口。README 不能代替素材 manifest。

当前只有 `00-sky/` 有拆层试产，其余层尚未正式交付。`previews/` 的整图只能做构图参考，不能反向当作分层成品。
