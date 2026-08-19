# AI 辅助游戏美术素材生产流水线

> 研究日期：2026-08-18（Asia/Shanghai）
>
> 范围：从现实原型或参考图，到可进入 2D 引擎的风格化/像素化透明素材。资料只采用论文、官方实现、官方产品文档或官方引擎手册。文中标为“建议”的内容是基于这些资料做出的项目流程推导，不是某个引擎的硬性规定。

## 结论

把 AI 当作“受约束的候选图生成器”，不要把它当作最终资产导出器。稳定的顺序是：

```text
来源与授权登记
  -> 参考图/现实原型整理
  -> 角度、构图、画布、占位和尺寸锁定
  -> 受控生成与风格化
  -> 固定像素网格、色板和透明边界
  -> 去背景/alpha 清理
  -> 尺寸、trim、pivot/anchor、命名和 manifest
  -> 引擎导入、图集构建、目标包验收
```

最重要的人工关口是：来源权利、透视/轮廓、接地与遮挡、风格与色板、透明边缘、pivot 对齐，以及目标设备上的最终观感。尺寸、格式、alpha、色板、命名、manifest 完整性和图集坐标适合自动化。

## 1. 来源、许可与可追溯性

先给每一张参考图、控制图、模型和输出分配一个不可变记录。至少记录：`asset_id`、`source_uri`、作者/权利人、许可证或服务条款、下载/生成日期、原文件 hash、模型与版本、提示词、seed、控制输入、人工审查人和审查结论。SPDX 官方建议使用标准化许可证 ID 表达许可信息，并强调许可证元数据用于沟通、分析和策略检查；这支持把许可字段放进素材 manifest，而不是只写在聊天记录里。（来源：[SPDX Handling License Info](https://spdx.dev/learn/handling-license-info/)，访问：2026-08-18）

ControlNet 官方实现仓库标为 Apache-2.0，但这只说明该仓库中适用的代码/仓库许可；不要据此推断所用基础模型、权重、训练数据或第三方参考图都具有相同许可。每次选模型都要单独保存模型卡和权利条款。（来源：[ControlNet 官方仓库](https://github.com/lllyasviel/ControlNet)，访问：2026-08-18）

**人工签字：** 参考图能否用于训练、输入、改编和发行；生成服务/模型条款是否允许商用；是否包含品牌、人物、车辆外观或第三方 IP。自动化只能检查字段存在和链接可访问，不能替代权利判断。

## 2. 现实原型/参考图到空间锁定

现实照片、3D 预览或线稿先不要直接交给风格化提示词。先产出一张“锁定控制图”，至少包含主体轮廓、关键边缘、深度或分割区域；需要车/角色固定姿态时再加入姿态或骨架控制。ControlNet 论文明确把边缘、深度、分割和人体姿态列为空间条件，并将其接入预训练文本到图像扩散模型，以便控制空间结构。（来源：[ControlNet 论文](https://arxiv.org/abs/2302.05543)，访问：2026-08-18；[ControlNet 官方实现](https://github.com/lllyasviel/ControlNet)，访问：2026-08-18）

在生成前建立一张 canonical sheet，锁定：

- 最终引擎画布尺寸和工作分辨率；
- 视角（如正后视、侧视）、相机高度、消失点、地面接触线；
- 主体的归一化 bounding box（`x/y/w/h`）和允许的裁切边界；
- 轮胎/脚/阴影的接地标记，以及碰撞盒或挂点的参考线；
- 背景是否只是控制图，还是要进入最终图层。

这一步的“尺寸和位置锁定”是项目工作流建议：生成模型仍可能改变细节，所以应在输出后自动比较主体框、关键点和控制图，再由人检查透视、遮挡和接地。自动比较通过只说明“偏离多少”，不能判断形体是否合理。

**可自动化：** 统一裁切到 canonical 画布；计算 alpha/分割后的主体框；检查主体框相对画布的偏差；将控制图和输出按同一坐标叠加生成审查图。

**人工审查：** 车轮是否落在同一地面、左右对称是否符合设计、前后比例是否被模型改写、关键灯/车窗/武器是否仍在约定位置。

## 3. 受控风格化

将已锁定的控制图作为结构条件，只改变风格变量：色板、线宽、材质、光源、时代感和背景层。ControlNet 的官方说明是“增加额外条件来控制扩散模型”，论文则说明空间条件可以与提示词组合；因此建议把“结构控制”和“风格提示”分成两个版本字段，避免用一条长 prompt 同时承担几何和画风。（来源：[ControlNet 官方仓库](https://github.com/lllyasviel/ControlNet)，访问：2026-08-18；[ControlNet 论文](https://arxiv.org/abs/2302.05543)，访问：2026-08-18）

一套素材至少保存三类中间产物：`control/`（边缘/深度/分割等）、`candidate/`（模型候选）、`approved/`（人工确认）。同一角色的不同角度应复用同一色板和 canonical sheet；先通过单张锚点，再批量生成变体。

**人工审查：** 画风是否属于本项目风格、颜色是否落在锁定色板、材质高光是否会在小尺寸下变成噪点、不同角度的设计是否仍被识别为同一物体。生成候选的数量、缩略图拼版、hash 和参数归档可自动化。

## 4. 像素/点阵化

像素化是一个确定的重采样和调色步骤，不是简单在 prompt 中写“pixel art”。建议先把 approved 候选缩到目标像素网格，再用最近邻放大到工作/展示尺寸；颜色压缩应使用项目色板，而不是让每张图产生一套新颜色。ImageMagick 官方文档说明 `-sample` 等价于 point（nearest-neighbor）重采样，`-colors`/`-posterize`/`-remap` 可减少颜色或映射到指定色板，且颜色减少算子可能产生抖动。（来源：[ImageMagick Command-line Options](https://imagemagick.org/command-line-options/)，访问：2026-08-18）

需要点阵而不需要渐变时，明确关闭或限制抖动；需要有意的半色调时，把抖动类型和强度作为 manifest 字段。像素网格、色板、抖动策略和允许的 alpha 级数必须先由人确认，再批处理同类资产。

运行时也要保持同一意图：Cocos Creator 3.8 的 Nearest 过滤只取最接近采样点的纹理单元，Linear 会平均相邻纹理单元并可能让像素游戏变模糊；Unity 的 Point（no filter）会让纹理近看保持块状；Godot 官方将 Lossless 作为 2D 默认并明确推荐用于 pixel art。（来源：[Cocos Creator 3.8 Texture Assets](https://docs.cocos.com/creator/3.8/manual/en/asset/texture.html)，访问：2026-08-18；[Unity Texture Importer](https://docs.unity3d.com/cn/2018.3/Manual/class-TextureImporter.html)，访问：2026-08-18；[Godot Importing Images](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)，访问：2026-08-18）

## 5. 去背景与透明 PNG

先保留 mask，再导出带 alpha 的 PNG。Adobe Photoshop 的官方 Remove Background 动作会隔离主体并创建透明背景或蒙版层，官方同时建议高对比输入，并在结果不完美时用画笔人工修正蒙版。（来源：[Adobe Remove Background](https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-background-in-your-images.html)，访问：2026-08-18）

背景处理建议分三层保存：原图、`mask`（灰度/alpha）、`cutout.png`（RGBA）。不要先把背景烤成纯色再靠色键删除，否则车灯、玻璃、雾和半透明阴影容易一起被删。ImageMagick 官方说明 alpha 通道可以启用、复制、提取或设为透明，也支持按颜色或邻接区域设为透明；这适合做可重复的批处理，但边缘取舍仍需要人工看棋盘格和高对比底色。（来源：[ImageMagick Alpha Options](https://imagemagick.org/command-line-options/)，访问：2026-08-18；[ImageMagick Image Masks](https://usage.imagemagick.org/masking/)，访问：2026-08-18）

**人工审查：** 轮胎内孔、车窗、天线、发光边缘、细线、半透明阴影和反射是否被误删；透明边缘是否带原背景色 halo；主体是否完整且不残留背景碎片。**可自动化：** 检查 PNG 是否含 alpha、透明像素占比、边缘颜色污染、mask 与 cutout 尺寸相同、是否出现全透明或全不透明异常。自动检测只能筛疑点，不能批准复杂边缘。

## 6. 尺寸、trim、pivot/anchor 与 manifest

建议同时保留两个尺寸：原始/设计画布尺寸和透明裁切后的 content rect。不要用“裁切后图片左上角”隐式代替锚点。

- **Cocos Creator 3.8：** `SpriteFrame` 记录 `rect`、`originalSize`、`pivot` 和 `offset`；其中 `offset` 用于说明透明裁切后的小矩形相对原中心的偏移。Sprite 组件又区分 Trimmed、Raw、Custom 三种尺寸模式。对需要世界坐标接地或碰撞对齐的车/角色，manifest 应明确使用原始画布、trimmed 还是 custom，并保存 pivot/offset。（来源：[Cocos Creator 3.8 SpriteFrame API](https://docs.cocos.com/creator/3.8/api/en/class/SpriteFrame)，访问：2026-08-18；[Cocos Sprite Component](https://docs.cocos.com/creator/3.8/manual/en/ui-system/components/editor/sprite.html)，访问：2026-08-18）
- **Unity：** 精灵导入设置包含 Sprite Mode 和 Pixels Per Unit；Sprite Editor 可切片并调整 sprite 的 pivot，pivot 是图形的坐标原点/锚点。图集 padding 用来降低相邻 sprite 之间的像素重叠，Atlas 的 filter mode 会覆盖图集中精灵的过滤设置。（来源：[Unity Sprite Import Settings](https://docs.unity3d.com/cn/current/Manual/texture-type-sprite.html)，访问：2026-08-18；[Unity Sprite Editor](https://docs.unity3d.com/cn/2023.2/Manual/SpriteEditor.html)，访问：2026-08-18；[Unity Sprite Atlas](https://docs.unity3d.com/cn/2018.3/Manual/class-SpriteAtlas.html)，访问：2026-08-18）
- **Godot：** `Sprite2D` 暴露 `centered`、`offset`、`region_rect` 等属性；`AtlasTexture` 用 `region` 从较大图集裁出子纹理，并有 `filter_clip` 以避免采样到区域外的周边像素。（来源：[Godot Sprite2D](https://docs.godotengine.org/en/stable/classes/class_sprite2d.html)，访问：2026-08-18；[Godot AtlasTexture](https://docs.godotengine.org/en/stable/classes/class_atlastexture.html)，访问：2026-08-18）

### 推荐 manifest（项目约定）

```json
{
  "asset_id": "car-racer-rear-v03",
  "file": "approved/cars/racer/rear-v03.png",
  "source_uri": ["..."],
  "license": "...",
  "source_hash": "sha256:...",
  "model": "...",
  "model_version": "...",
  "prompt_hash": "sha256:...",
  "control_inputs": ["edge", "depth"],
  "canvas_px": [256, 256],
  "content_rect_px": [42, 31, 172, 208],
  "pivot_norm": [0.5, 0.93],
  "pixels_per_unit": 100,
  "trim": "preserve-original-canvas",
  "filter": "nearest",
  "mipmaps": false,
  "atlas": {"name": "cars", "padding_px": 2, "allow_rotation": false},
  "engine_refs": {"cocos_sprite_frame": "db://assets/..."},
  "human_review": {"status": "approved", "reviewer": "...", "date": "2026-08-18"}
}
```

字段命名是本项目建议；`pivot_norm` 用 0–1 的画布归一化坐标，运行时再转换成具体引擎的 pivot/offset/PPU。这样同一份来源、尺寸和锚点信息可以喂给 Cocos、Unity 或 Godot，而不是把关键信息藏在某个编辑器面板里。

## 7. 图集、导入和目标包

### Cocos Creator 3.8（本项目主线）

Cocos 导入资产会生成同名 `.meta`，其中包含 UUID、贴图裁切数据和其他配置；官方明确建议通过编辑器管理移动/重命名，以保持 UUID 和引用稳定。将 PNG 放入 `assets/` 后应等待 Creator reimport，再在 Inspector 核对 SpriteFrame、Trim、Filter、Wrap、Size Mode 和 pivot/offset。（来源：[Cocos Creator 3.8 Assets Workflow](https://docs.cocos.com/creator/3.8/manual/en/asset/asset-workflow.html)，访问：2026-08-18）

Auto Atlas 会把指定目录的 SpriteFrame 在构建时打包；编辑器和预览仍使用拆分的 SpriteFrame，只有 build 后才生成并使用 atlas。Auto Atlas 提供最大宽高、padding、是否旋转、Power of Two、Padding Bleed 等选项，并保留原 SpriteFrame 配置。因此预览通过不等于最终图集通过，必须对导出包做一次验证。（来源：[Cocos Creator 3.8 Auto Atlas](https://docs.cocos.com/creator/3.8/manual/en/asset/auto-atlas.html)，访问：2026-08-18）

像素素材默认使用 Nearest，透明精灵检查 Clamp-to-edge；Cocos 官方说明 SpriteFrame 类型会自动将 Wrap Mode 调整为 clamp-to-edge，但项目若改了设置仍需在验收中复核。纹理压缩应按目标平台和 alpha 情况检查，Cocos 构建会根据透明通道筛选可用压缩格式。（来源：[Cocos Creator 3.8 Texture Assets](https://docs.cocos.com/creator/3.8/manual/en/asset/texture.html)，访问：2026-08-18；[Cocos Creator 3.8 Compressed Textures](https://docs.cocos.com/creator/3.8/manual/en/asset/compress-texture.html)，访问：2026-08-18）

### Unity / Godot 对照

Unity 的基本链路是：导入为 Sprite (2D and UI) -> Single/Multiple -> Sprite Editor 切片和 pivot -> Sprite Atlas 配置 -> build。图集的 `Include in Build`、padding、rotation 和 filter mode 都是可检查的构建参数；UI 或方向敏感图像应谨慎允许 rotation。（来源：[Unity Sprite Import Settings](https://docs.unity3d.com/cn/current/Manual/texture-type-sprite.html)，访问：2026-08-18；[Unity Sprite Atlas](https://docs.unity3d.com/cn/2018.3/Manual/class-SpriteAtlas.html)，访问：2026-08-18）

Godot 的基本链路是：把 PNG 放进项目目录 -> editor import/reimport -> Texture2D 或 TextureAtlas -> Sprite2D/AtlasTexture -> 导出项目。官方说明 Godot 会在项目中自动导入并生成 `.import` 配置，且这些配置应纳入版本控制；运行时代码应使用 Resource Loader 访问已导入资源，而不是用文件系统路径读取内部导入物。（来源：[Godot Import Process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html)，访问：2026-08-18；[Godot Importing Images](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)，访问：2026-08-18）

## 8. 自动化与人工审查边界

| 环节 | 可自动化 | 必须人工确认 |
| --- | --- | --- |
| 来源 | manifest 字段完整、URL/hash/日期存在、许可证 ID 格式化 | 是否有权使用、服务条款是否允许发行、第三方 IP 风险 |
| 结构锁定 | 画布尺寸、主体框偏差、关键点偏差、控制图与输出叠图 | 透视、轮胎/脚接地、遮挡、形体辨识度 |
| 风格化 | 候选批量生成、参数/seed 归档、色板距离统计 | 风格一致性、材质读法、不同角度是否像同一物体 |
| 像素化 | 最近邻缩放、色板映射、颜色数、抖动参数、整数倍尺寸 | 小尺寸可读性、关键细节是否变噪点、边缘是否断裂 |
| 透明 | PNG/RGBA/alpha 检查、全透明异常、mask 尺寸和 hash | 毛发/玻璃/发光/阴影边缘、背景 halo、漏删背景 |
| frame/anchor | rect 越界、pivot 范围、PPU/画布尺寸、命名冲突 | 接地和碰撞挂点、trim 后是否跳位、镜像/旋转后的语义 |
| 图集/引擎 | padding、旋转开关、filter/wrap、构建是否含资源、导入错误日志 | 目标分辨率真机截图、动画帧不抖、最终色彩/透明观感 |

## 9. 验收清单与常见失败模式

### 机器检查（每次提交）

1. 用图像工具检查文件格式、宽高、颜色数、alpha 通道和全透明/全不透明异常；ImageMagick 官方 `identify` 支持读取图像属性和 alpha 相关选项。（来源：[ImageMagick Identify](https://imagemagick.org/identify/)，访问：2026-08-18）
2. 校验文件 hash 与 manifest；校验 `canvas_px`、`content_rect_px`、pivot、PPU、filter、mipmap、atlas 名和 padding 均存在。
3. 检查主体框相对 canonical sheet 的偏差；检查 atlas 每个 rect 不越界、名称唯一、padding 足够，禁止旋转的资产不能被图集旋转。
4. Cocos：导入后确认 `.meta` 与 PNG 成对、UUID 稳定；build 后确认 Auto Atlas 真被使用，且包中没有因错误引用产生的重复大图。（来源：[Cocos Assets Workflow](https://docs.cocos.com/creator/3.8/manual/en/asset/asset-workflow.html)，访问：2026-08-18；[Cocos Auto Atlas](https://docs.cocos.com/creator/3.8/manual/en/asset/auto-atlas.html)，访问：2026-08-18）
5. 在目标画布和至少一个真实目标设备/模拟器运行 smoke scene：显示单图、trimmed/raw 对照、pivot 接地、atlas 子图、透明底、Nearest 放大、动画首尾帧和导出包加载。

### 常见失败模式

- **生成漂移：** 角度、轮胎位置、比例或车灯在候选间变化。原因是只靠 prompt，没有边缘/深度/分割/姿态控制。修复是固定 canonical sheet 和控制图；机器先筛偏差，人再判定形体。（依据：[ControlNet 论文](https://arxiv.org/abs/2302.05543)，访问：2026-08-18）
- **背景残留/halo：** 去背景后边缘带天空色或把玻璃、灯光一起删掉。高对比输入有助于自动动作，但 Adobe 仍要求对不完美 mask 手工修正；保留 mask 和原图可回溯。（来源：[Adobe Remove Background](https://helpx.adobe.com/photoshop/desktop/repair-retouch/remove-objects-fill-space/remove-background-in-your-images.html)，访问：2026-08-18）
- **像素模糊或闪烁：** 使用 Linear、mipmap、非整数缩放或有损/VRAM 压缩。Cocos 说明 Linear 可能使像素游戏模糊；Godot 明确提醒 VRAM 压缩会在低分辨率 2D/pixel art 中产生明显伪影；Unity Point 过滤用于保留块状效果。（来源：[Cocos Texture Assets](https://docs.cocos.com/creator/3.8/manual/en/asset/texture.html)，访问：2026-08-18；[Godot Importing Images](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)，访问：2026-08-18；[Unity Texture Importer](https://docs.unity3d.com/cn/2018.3/Manual/class-TextureImporter.html)，访问：2026-08-18）
- **图集串色/边缘 bleeding：** padding 太小、采样到邻图、区域外过滤未裁切。Cocos Auto Atlas 提供 Padding/Padding Bleed，Unity 用 padding 防止相邻像素重叠，Godot AtlasTexture 提供 `filter_clip`；按目标引擎配置并在放大截图中验收。（来源：[Cocos Auto Atlas](https://docs.cocos.com/creator/3.8/manual/en/asset/auto-atlas.html)，访问：2026-08-18；[Unity Sprite Atlas](https://docs.unity3d.com/cn/2018.3/Manual/class-SpriteAtlas.html)，访问：2026-08-18；[Godot AtlasTexture](https://docs.godotengine.org/en/stable/classes/class_atlastexture.html)，访问：2026-08-18）
- **trim 导致角色跳位：** 透明边被裁掉后，直接以裁切图左上角或中心作为挂点。Cocos 的 `originalSize`/`offset` 和 Sprite 的 Raw/Trimmed/Custom 模式说明了这个差异；Unity/Godot 也分别把 pivot/offset 暴露为独立属性。修复是把原始画布、content rect 和 pivot 写入 manifest，运行时只引用明确的模式。（来源：[Cocos SpriteFrame API](https://docs.cocos.com/creator/3.8/api/en/class/SpriteFrame)，访问：2026-08-18；[Unity Sprite Editor](https://docs.unity3d.com/cn/2023.2/Manual/SpriteEditor.html)，访问：2026-08-18；[Godot Sprite2D](https://docs.godotengine.org/en/stable/classes/class_sprite2d.html)，访问：2026-08-18）
- **引擎引用断裂：** 在文件管理器中移动/复制 Cocos 资产但漏掉 `.meta`，或在 Godot 导出项目中把内部导入文件当普通路径读取。修复是用 Cocos Assets 面板管理资源，提交 `.meta`；Godot 使用 Resource Loader 并提交 `.import` 配置。（来源：[Cocos Assets Workflow](https://docs.cocos.com/creator/3.8/manual/en/asset/asset-workflow.html)，访问：2026-08-18；[Godot Import Process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html)，访问：2026-08-18）
- **只验编辑器、不验构建包：** Cocos Auto Atlas 在编辑器/预览中仍用拆分 SpriteFrame，build 后才生成 atlas；因此编辑器看起来正确不能证明导出包的图集、压缩和加载路径正确。（来源：[Cocos Auto Atlas](https://docs.cocos.com/creator/3.8/manual/en/asset/auto-atlas.html)，访问：2026-08-18）

## 10. 适用于本项目的最小落地版本

1. 每辆车先做一个角度锚点：canonical sheet、edge/depth 控制图、approved RGBA PNG 和一份 manifest。
2. 锚点通过人工审查后，再批量生成侧视/三分之四视图；批量只改变风格和动作变量，不改变画布、主体框和接地线。
3. 用固定像素网格和项目色板执行缩放、颜色映射、抖动；保留原图、mask、像素化中间图和最终 PNG。
4. 先以拆分 PNG 导入 Cocos 验证 SpriteFrame/pivot/接地，再创建 Auto Atlas；build 后重新验证图集、纹理过滤、透明边缘和微信小游戏包。
5. 任何自动检查失败，或人工关口未签字，素材停留在 `candidate/`，不得进入运行时资产目录。

