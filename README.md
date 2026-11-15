# 大叔汪短剧技能包

版本：V0.4-testing

系统只保留三个核心阶段：

1. 小说改编成可执行短剧剧本。
2. 从剧本生成必要的完整符资产提示词并锁定资产。
3. 使用剧本与已确认符资产生成视频提示词，并按选择接入 Vidu Q4 闲时创作或 Seedance 平台路线。

V0.4 新增开工七问、改编试写门、完整资产格式与看图验收、12—16 秒高密度生成组、动作—对白锚点、Vidu Q4 闲时安全执行、任务去重、无水印下载、分层质检和真实完成等级。Vidu 闲时只有实时资格有效且精确 0 积分时才能提交，不提供收费兜底。

工作期间会按真实阶段显示“大叔汪干活碎碎念”：以上班族、冷笑话、片场和电脑等待为主，少量穿插生活与吃喝吐槽；不展示隐藏推理，也不使用玩笑虚报进度。

## 发行版本

### Codex 版

目录：`codex/ai-drama-production/`

包含标准 `SKILL.md`、完整模块资源和 Codex 的 `agents/openai.yaml` 界面元数据。

用户级安装：将 `ai-drama-production` 整个目录复制到：

- Windows：`%USERPROFILE%\.codex\skills\ai-drama-production\`
- macOS/Linux：`~/.codex/skills/ai-drama-production/`

安装后新开一个 Codex 任务，在同一条消息里贴原著位置，加一句启动语：

```text
"C:\短剧项目\原著"
大叔汪开始做新剧
```

也可以把第一行换成小说文件的完整路径，或当前项目中唯一的文件名（如 `我的小说.txt`）。只有一份可读原著就直接开始读，多份才请你选；只询问还没定的开工项。这句启动语不自动授权远程生成或积分消费。

### WorkBuddy / Agent Skills 通用版

目录：`workbuddy-universal/ai-drama-production/`

移除了 Codex 专用界面元数据，只保留通用 `SKILL.md`、模块、引用、Schema、模板和校验脚本。

WorkBuddy 项目级安装：复制到项目目录：

```text
.codebuddy/skills/ai-drama-production/
```

也可以在 WorkBuddy 的 Skill 管理页面选择“导入 Skill”。安装后通过 `/` 选择技能，或直接输入与 Codex 相同的启动提示词。

## ZIP 包

- `dist/大叔汪短剧技能包-Codex-V0.4-testing.zip`
- `dist/大叔汪短剧技能包-WorkBuddy通用版-V0.4-testing.zip`

## 项目原则

- 符就是资产，包含资产符与技能符。
- 不从长篇原文直接跳到最终视频提示词。
- 每个入选资产都使用完整独立冻结模板，不写“同上”。
- 只制作用于辨识度、连续性或反复使用所必需的符。
- 源提示词与平台执行载荷分开，平台适配不得改写剧情或对白。
- 单个测试剧的数据不得写入通用 Skill。
- 不为暂时用不到的功能增加复杂系统层。

## 官方格式参考

- Codex Skill 示例与结构：https://github.com/openai/codex/tree/main/codex-rs/skills/src/assets/samples
- WorkBuddy Skills：https://cloud.tencent.com/document/product/1831/134516
