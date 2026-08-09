---
name: ai-drama-production
description: 将小说、网文、故事梗概或原创剧情转化为 AI 短剧生产结果，核心覆盖小说改编成可拍脚本、为人物/场景/道具/技能等符资产生成可复制的生图提示词，以及使用脚本和已确认符资产生成视频模型提示词。用于小说改编短剧、符资产制作、15 秒视频镜头提示词和连续剧生产；不得跳过脚本与关键资产确认直接从长篇原文生成最终视频提示词。
---

# AI Drama Production

只维护三个不可或缺的核心阶段。辅助规则只用于保证连续性和可修改性，不得扩张成独立复杂系统。

## 开始前

1. 读取 `PROJECT_KNOWLEDGE_BASE.md` 和 `core/workflow.md`。
2. 只读取当前阶段需要的模块与 Schema，不预加载无关资料。
3. 涉及制符时，读取 `modules/rune_generation/` 的总规范和对应模板；不得凭记忆简化格式。
4. 涉及视频提示词时，读取 `modules/shot_design/` 和所选 `modules/prompt_engine/` 方法。

## 三个核心阶段

### 1. 小说改编成脚本

调用 `modules/adaptation/`，理解原文后输出分集、场次、人物动作、原样对白、情绪、冲突和集尾钩子。短剧按有效剧情拍点分配时长；约 15 秒片段通常包含 3—5 个因果连续微拍点。先由用户确认改编方向和脚本，再进入资产制作。

### 2. 脚本生成符资产提示词

从已确认脚本中找出必须保持一致或反复使用的人物、服装、场景、道具、生物、界面、特效与技能方法。先复用已有符；只为必要对象创建或升级符。调用 `modules/rune_generation/` 输出可直接复制到生图模型的完整提示词，并由用户确认关键符资产。

### 3. 脚本与符生成视频

调用 `modules/shot_design/` 将脚本拆成可生成片段，再调用 `modules/prompt_engine/` 生成视频提示词。提示词必须明确装载的符、人物与场景当前状态、动作—对白同步、镜头调度和片段最终目标。目标模型有特殊限制时再调用 `modules/model_adapter/`，不得改变脚本事实或符身份。

## 不可偏离的规则

- 符就是资产，包含资产符和技能符；不是所有流程都要变成符。
- 制符提示词必须保持已冻结的 `【】` 分区与横向信息资产板格式，不得退化为关键词堆砌或普通概念图。
- 关键人物、核心场景、关键道具和标志性技能优先制符；一次性且无连续性要求的背景元素直接写进镜头提示词。
- 对白不得擅自改写；边做边说的台词必须绑定动作节点。
- 约 15 秒是生成容器，不得用慢动作、停顿或空镜把 3—5 秒内容强行拉满。
- 重要符使用唯一 ID；已批准资产修改时保留旧版并建立新版本。
- 单部剧只作为测试样本，不得把其人物、场景或剧情写入本 Skill。

## 轻量辅助

- 资产表：只记录符 ID、类型、版本、状态和使用位置。
- 质量检查：只检查脚本因果、符一致性、动作对白、镜头节奏和模型可执行性。
- 人工确认：只保留脚本方向、关键符、最终视频提示词三个确认点。
- 工作台、批处理、自动回流和多模型执行均为后续可选能力，不是当前核心。

## 读取路由

- 三阶段边界与验收：`references/core-scope-and-acceptance-v0.3.md`
- 执行和版本规则：`core/execution_rules.md`、`core/version_manager.md`
- 改编与短剧节奏：`modules/adaptation/README.md`、`modules/adaptation/short_drama_pacing_v0.2.md`
- 必要资产判断：`modules/asset_analysis/decision_method_v0.2.md`
- 制符：`modules/rune_generation/README.md` 及对应模板
- 15 秒镜头：`modules/shot_design/vertical_short_drama_shot_v0.2.md`
- 视频提示词：`modules/prompt_engine/README.md` 及所选模式
- 数据格式：只读取当前输出对应的 `schemas/`
