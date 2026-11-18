# Vidu 直连提交门禁：本地记录

提交前从已验证的直连能力、实际载荷和本次实时零费核对填入下表。示例是假数据，**不可拷作提交证据**。命令：`python scripts/check_vidu_direct.py <本地预检记录.json>`。通过只是本地证据结构合格；仍需授权并只能向核对过的接口提交相同载荷。

```json
{
  "route": {"transport":"frame_direct","model_version":"实际版本","generation_type":"实际类型","schedule_mode":"nopeak","audio_mode":"native_prompt_audio"},
  "sound_plan":"native_audible_audio",
  "sound_in_prompt":true,
  "payload_sha256":"实际执行载荷的 64 位小写十六进制摘要",
  "native_audio_output":{
    "status":"supported",
    "source":"same_route_original",
    "route":{"transport":"frame_direct","model_version":"实际版本","generation_type":"实际类型","schedule_mode":"nopeak","audio_mode":"native_prompt_audio"},
    "evidence_ref":"同路线真实原片验收记录",
    "task_id":"原任务 ID",
    "original_audio_stream":true,
    "original_audio_audible":true
  },
  "live_zero_cost":{
    "route":{"transport":"frame_direct","model_version":"实际版本","generation_type":"实际类型","schedule_mode":"nopeak","audio_mode":"native_prompt_audio"},
    "payload_sha256":"同一实际执行载荷摘要",
    "evidence_ref":"本次报价 ID 或当前直连实时额度回读记录的位置",
    "valid_now":true,
    "cost_credits":0,
    "remaining":1
  }
}
```

- `transport` 只能为 `frame_direct` 或 `vidu_cli_direct`。`audio_mode: native_prompt_audio` 表示实际载荷用提示词要求随片原音，不表示音频驱动对口型，也不是供应方参数。路线记录须完全一致；有影响音频输出的模式或设置变化时重查，不沿用旧证据。原生音轨来源不明、证据只证明有音频输入、不同工具或生成模式的样片，均不算通过。
- 若直连接口明确说明当前模式支持原音随视频输出，可以把 `source` 改为 `explicit_output_capability`，加 `explicitly_confirms_output: true`，用 `evidence_ref` 指向实际能力回读，省略三项原片字段。若返回 `audioSupportedInThisNode: false`，既不写输出 `unsupported`，也不当作输出 `supported`。
- 只按实时回读填写费用和剩余额度。`valid_now` 不是默认值：重提交、改载荷、额度变化或资格过期后重新核对。只有平台实时额度记录而无逐载荷报价时，载荷摘要是本地绑定，不能把它说成平台报价。保存检查输出；不通过时不创建生成任务，不打开网页、不改成静音或付费。
