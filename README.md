# 大叔汪短剧技能包

版本：V0.3-testing（MVP）

用于完成三个连续阶段：

1. 小说改编成可拍短剧脚本。
2. 从脚本生成必要符资产及可复制的制符提示词。
3. 使用脚本和已确认符资产生成视频模型提示词。

这是有人参与三个确认点的生产型 MVP：脚本确认、关键符确认、最终视频提示词确认。当前不包含一键调用生图/视频模型、自动剪辑或工作台。

## 发行版本

### Codex 版

目录：`codex/ai-drama-production/`

包含标准 `SKILL.md`、完整模块资源和 Codex 的 `agents/openai.yaml` 界面元数据。

用户级安装：将 `ai-drama-production` 整个目录复制到：

- Windows：`%USERPROFILE%\.codex\skills\ai-drama-production\`
- macOS/Linux：`~/.codex/skills/ai-drama-production/`

安装后新开一个 Codex 任务，输入：

```text
使用 $ai-drama-production 开始一个新的短剧项目。
小说文件：<文件路径>
成片：9:16竖屏，每集约2分钟。
先执行Stage 1，只输出整体改编方案和第一集脚本，等我确认后再制符。
```

### WorkBuddy / Agent Skills 通用版

目录：`workbuddy-universal/ai-drama-production/`

移除了 Codex 专用界面元数据，只保留通用 `SKILL.md`、模块、引用、Schema 和模板。

WorkBuddy 项目级安装：复制到项目目录：

```text
.codebuddy/skills/ai-drama-production/
```

也可以在 WorkBuddy 的 Skill 管理页面选择“导入 Skill”。安装后通过 `/` 选择技能，或直接输入与 Codex 相同的启动提示词。

## ZIP 包

- `dist/大叔汪短剧技能包-Codex-V0.3-testing.zip`
- `dist/大叔汪短剧技能包-WorkBuddy通用版-V0.3-testing.zip`

## 项目原则

- 符就是资产，包含资产符与技能符。
- 不从长篇原文直接跳到最终视频提示词。
- 只制作用于辨识度、连续性或反复使用所必需的符。
- 单个测试剧的数据不得写入通用 Skill。
- 不为暂时用不到的功能增加复杂系统层。

## 官方格式参考

- Codex Skill 示例与结构：https://github.com/openai/codex/tree/main/codex-rs/skills/src/assets/samples
- WorkBuddy Skills：https://cloud.tencent.com/document/product/1831/134516
