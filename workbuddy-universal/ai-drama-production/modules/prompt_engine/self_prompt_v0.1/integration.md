# Prompt Engine 集成约定

## 模块身份

- 方法名：`self_prompt_engine`
- 版本：`V0.1`
- 模式：`self`
- 当前状态：`testing`，用户确认暂时保留 A 版，后续以新版本迭代。
- 上游：已批准 `shot_database`、`asset_registry`、`project_config`。
- 下游：`model_adapter`、视频生成与质量审核。

## 输入

至少读取：

- `shot_id`、`duration`、`story_goal`、`emotion_goal`。
- 人物及 `character_states` 的精确状态标注。
- 场景名称、时间、环境状态。
- 实际装载的人物、场景、道具、技能、声音和视频资产及版本。
- Shot 中已确认的动作、表演、对白、摄影、光影和声音信息。
- `continuity.start_state`、`continuity.end_state`、`continuity.next_connection`。
- 项目全局风格和本镜覆盖项。

缺少必需输入时返回缺失项，不填充最终提示词。

## 输出

生成一个符合现有 `prompt_schema.json` 的记录：

```json
{
  "prompt_id": "<shot_id>_SELF_V0.1_<revision>",
  "shot_id": "<shot_id>",
  "engine_version": "self_prompt_engine_V0.1",
  "mode": "self",
  "input_data": {
    "shot_version": "<version>",
    "asset_versions": {},
    "project_config_version": "<version>"
  },
  "prompt_text": "<固定四区全文>",
  "negative_constraints": [],
  "review": {},
  "version": "V0.1"
}
```

`prompt_text` 必须包含完整四区，而不是只保存 `【提示词】`正文。`negative_constraints`可以保存结构化审核数据，但正文仍应自然语言写入本镜头真正需要的视频模型限制。

## 与 ai-drama-production 的边界

- 不修改故事事实、人物身份、资产版本、对白或 Shot 目标。
- 不负责生成或修改符，只消费已确认资产。
- 不负责重新设计 Shot；发现容量、对白或连续性问题时退回 `shot_design`。
- `model_adapter`只能适配目标模型的表达和参数，不得删除四区职责、精确状态绑定、开头承接或结尾目标。
- `dual`模式可以并行调用本模块和 TD 模块，分别保留独立版本，不得把两种方法混成一个不可追溯文本。

## 推荐集成方式

本版本固定安装于：

```text
modules/prompt_engine/
└── self_prompt_v0.1/
    ├── method.md
    ├── dialogue_demo.md
    └── integration.md
```

三份文件分别作为方法标准、对白示例和集成约定使用。升级 self 方法时新增版本目录并更新路由，不覆盖本目录；control、TD 与 dual 继续独立版本化。

