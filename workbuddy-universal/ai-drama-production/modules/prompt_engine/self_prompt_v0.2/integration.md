# Self V0.2 集成约定

上游为已批准 `shot_database`、`asset_registry`、`project_config`；下游为模型适配、生成与审核。`control`、`td`、`dual` 仍独立保留，不声称已经实现。

除 Shot、动作—对白锚点、连续性和风格外，每位出镜角色必须关联本组适用的已穿装角色图。使用现有 `input_data` 保存引用，不新增资产系统或顶层 Schema。

```json
{
  "prompt_id": "S01E01-G01_SELF_V0.2_01",
  "shot_id": "S01E01-G01",
  "engine_version": "self_prompt_engine_V0.2",
  "mode": "self",
  "input_data": {
    "shot_version": "V1",
    "project_config_version": "V1",
    "asset_versions": {"CH001_LOOK02": "V1"},
    "character_references": [
      {
        "character_id": "CH001",
        "asset_id": "CH001_LOOK02",
        "asset_version": "V1",
        "file": "assets/characters/CH001_LOOK02_V1.png",
        "reference_order": 1,
        "outfit_matches_shot": true,
        "confirmed": true
      }
    ]
  },
  "prompt_text": "<完整四区；例中的路径和确认值为演示，不是实际装载证据>",
  "negative_constraints": [],
  "review": {},
  "version": "V0.2"
}
```

适配器逐组读取实际文件、核对图片与已批准衣装／状态，并将人物引用按序映射到平台真实上传清单。`outfit_matches_shot` 和 `confirmed` 是有依据的审核记录，不是填 `true` 即可的能力证明；实际提交另记上传身份、顺序和任务 ID。只有审核稿时标待装载，不提前记已上传。衣装检查发生在内部资产对照，四区源稿和派生执行提示词都不重新复述服装设计。

参考缺失、衣装不符、图未确认、版本与文件不一致或参考数超限时，不提交，回到资产或分镜处理。镜内换装／破损变化逐个记录所需的前后状态图和相应节点，不用上例的单图代替。提示词只写必要动作与精确状态，不用衣装形容词补缺图。

当前这些是 Skill 执行与人工／模型审核要求，不声称平台服务端已有自动验装识别。原有 Vidu 直连零费原音门禁不替代本项审核，音频、额度及费用规则保持不变。

本目录作为新输出默认；旧 `self_prompt_v0.1/` 原样保留。续作保留已批准旧稿，新稿采用 V0.2 须另存并重审，不能仅改引擎标记。
