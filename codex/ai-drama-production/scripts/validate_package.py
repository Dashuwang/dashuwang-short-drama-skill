#!/usr/bin/env python3
"""Validate the lean three-stage AI drama skill package."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check_character_examples(root: Path, errors: list[str]) -> None:
    fields = (
        "人物ID,角色名,身份,性别,视觉年龄,身高厘米,脸型与下颌,颧骨,眉形,眼形与眼距,鼻形,唇形,"
        "肤色与年龄感,身材体态,发型,默认服装与鞋履,易混人物ID,主要区分点,原著或底稿依据,"
        "制作设定说明,人设母版版本,对照状态"
    ).split(",")
    template = root / "templates/character_differentiation.template.csv"
    example = root / "examples/character_differentiation.example.csv"
    prompts = root / "examples/character_differentiation_prompts.md"
    standard = root / "modules/rune_generation/asset_prompt_format_v0.5.md"
    if not all(path.is_file() for path in (template, example, prompts, standard)):
        return
    rows = []
    for path in (template, example):
        if not path.read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append(f"CSV missing UTF-8 BOM: {path.name}")
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != fields:
                errors.append(f"CSV header differs from character contract: {path.name}")
                return
            rows = list(reader)
        if path == template and rows:
            errors.append("Blank character CSV template must not contain example rows")
    ids = {row["人物ID"] for row in rows}
    if len(rows) != 2 or len(ids) != 2 or any(
        None in row or any(not row[field] for field in fields)
        or row["易混人物ID"] not in ids - {row["人物ID"]}
        or row["对照状态"] != "已完成文字对照" for row in rows
    ):
        errors.append("Character demo must contain two complete reciprocal comparison rows")
        return
    if rows[0]["默认服装与鞋履"] != rows[1]["默认服装与鞋履"] or not all(
        rows[0][field] != rows[1][field] for field in ("脸型与下颌", "眼形与眼距", "身材体态")
    ):
        errors.append("Character demo must contrast facial/body anchors without changing uniform")
    section_names = re.findall(r"^\d+\. `(【[^】]+】)`", standard.read_text(encoding="utf-8"), re.M)
    blocks = re.findall(r"^```text\n(.*?)^```", prompts.read_text(encoding="utf-8"), re.M | re.S)
    if len(section_names) != 20 or len(blocks) != len(rows):
        errors.append("Missing complete 20-section prompts for character demo")
        return
    for row, block in zip(rows, blocks):
        if re.findall(r"^【[^】]+】", block, re.M) != section_names or not all(
            row[key] in block for key in ("人物ID", "角色名", "视觉年龄", "身高厘米")
        ) or any(token in block for token in ("参见差异表", "同上")):
            errors.append(f"Incomplete standalone character prompt: {row['人物ID']}")


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors: list[str] = []

    required = [
        "SKILL.md",
        "VERSION",
        "PROJECT_KNOWLEDGE_BASE.md",
        "core/workflow.md",
        "core/execution_rules.md",
        "core/quality_check.md",
        "references/core-scope-and-acceptance-v0.3.md",
        "references/project-intake-and-routing-v0.4.md",
        "references/project-intake-and-routing-v0.5.md",
        "assets/project-intake.html",
        "modules/adaptation/screenplay_format_v0.5.md",
        "modules/rune_generation/asset_prompt_format_v0.5.md",
        "modules/rune_generation/character_differentiation_v0.1.md",
        "templates/character_differentiation.template.csv",
        "examples/character_differentiation.example.csv",
        "examples/character_differentiation_prompts.md",
        "references/end-to-end-production-flow-v0.4.md",
        "references/proven-production-rules-v0.4.md",
        "references/work-status-copy-v0.1.md",
        "modules/asset_analysis/decision_method_v0.2.md",
        "modules/rune_generation/production_asset_standard_v0.4.md",
        "modules/model_adapter/vidu_nopeak_v0.1.md",
        "scripts/check_vidu_direct.py",
        "scripts/vidu_direct_gate.md",
        "templates/project_intake.template.json",
        "templates/current.template.json",
        "config/work_status_copy_v0.1.json",
        "schemas/asset_analysis_result_schema.json",
        "examples/asset_analysis_minimal.json",
    ]
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        content = skill_path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            errors.append("SKILL.md has invalid frontmatter")
        else:
            frontmatter = match.group(1)
            if not re.search(r"^name:\s*ai-drama-production$", frontmatter, re.MULTILINE):
                errors.append("SKILL.md name must be ai-drama-production")
            if not re.search(r"^description:\s*\S+", frontmatter, re.MULTILINE):
                errors.append("SKILL.md description is missing")
        for phrase in ("小说改编成脚本", "脚本生成符资产提示词", "脚本与符生成视频", "vidu_nopeak", "大叔汪开始做新剧"):
            if phrase not in content:
                errors.append(f"SKILL.md missing core stage: {phrase}")

    version_path = root / "VERSION"
    if version_path.is_file() and version_path.read_text(encoding="utf-8").strip() != "V0.5.3-testing":
        errors.append("VERSION must be V0.5.3-testing")

    interface_path = root / "agents/openai.yaml"
    if interface_path.is_file():
        interface = interface_path.read_text(encoding="utf-8")
        if "$ai-drama-production" not in interface or "�" in interface:
            errors.append("agents/openai.yaml is invalid or stale")

    for path in root.rglob("*.json"):
        try:
            load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON {path.relative_to(root)}: {exc}")

    manifest_path = root / "modules/asset_analysis/manifest.json"
    if manifest_path.is_file():
        manifest = load_json(manifest_path)
        if manifest.get("version") != "V0.2" or manifest.get("status") != "testing":
            errors.append("asset_analysis must remain V0.2-testing")
        if manifest.get("input") != ["approved_script", "existing_asset_registry"]:
            errors.append("asset_analysis input must stay lean")

    example_path = root / "examples/asset_analysis_minimal.json"
    if example_path.is_file():
        example = load_json(example_path)
        if example.get("module_version") != "V0.2":
            errors.append("asset analysis example must use V0.2")
        for item in example.get("required_runes", []):
            for key in ("candidate_id", "canonical_key", "source_ref", "reason", "decision"):
                if not item.get(key):
                    errors.append(f"asset analysis example missing {key}")
            if "scores" in item or "dependencies" in item:
                errors.append("asset analysis example contains removed complexity")

    registry_path = root / "templates/asset_registry.template.json"
    if registry_path.is_file():
        registry = load_json(registry_path)
        required_keys = {"asset_id", "asset_name", "canonical_key", "asset_type", "importance", "status", "version"}
        if not required_keys.issubset(registry):
            errors.append("asset registry template is incomplete")
        if "dependencies" in registry or "approval" in registry:
            errors.append("asset registry template contains removed complexity")

    intake_path = root / "templates/project_intake.template.json"
    if intake_path.is_file():
        intake = load_json(intake_path)
        required_intake = {
            "source",
            "adaptation_policy",
            "visual_style",
            "genre",
            "audience_lane",
            "ratio",
            "episode_duration_seconds",
            "episode_count_or_total_duration",
            "production_route",
            "seedance_platform",
            "special_requirements",
        }
        if not required_intake.issubset(intake):
            errors.append("project intake template is incomplete")

    adapter_manifest_path = root / "modules/model_adapter/manifest.json"
    if adapter_manifest_path.is_file():
        adapter = load_json(adapter_manifest_path)
        route = adapter.get("routes", {}).get("vidu_nopeak", {})
        if adapter.get("status") != "testing" or route.get("entrypoint") != "vidu_nopeak_v0.1.md":
            errors.append("model_adapter Vidu nopeak route is missing or inactive")
        if (route.get("preflight_gate") != "scripts/check_vidu_direct.py"
                or route.get("allowed_transports") != ["frame_direct", "vidu_cli_direct"]
                or route.get("requires_audible_native_audio") is not True):
            errors.append("model_adapter must require the direct-only native-audio gate")

    asset_standard_path = root / "modules/rune_generation/production_asset_standard_v0.4.md"
    if asset_standard_path.is_file():
        standard = asset_standard_path.read_text(encoding="utf-8")
        for phrase in ("完整、独立、可复制", "不得使用“同上”", "人物状态与年龄变体"):
            if phrase not in standard:
                errors.append(f"asset standard missing frozen requirement: {phrase}")

    status_copy_path = root / "config/work_status_copy_v0.1.json"
    if status_copy_path.is_file():
        status_copy = load_json(status_copy_path)
        weights = status_copy.get("weights", {})
        if sum(weights.values()) != 100:
            errors.append("work status copy weights must total 100")
        if weights.get("food_drink") != 10:
            errors.append("food and drink status copy must remain a minority")
        if not status_copy.get("max_one_line_per_meaningful_stage"):
            errors.append("work status copy must be rate limited")

    obsolete = [
        "references/system-capability-matrix-v0.3.md",
        "references/acceptance-test-matrix-v0.3.md",
        "README_FOR_CODEX.md",
        "CHANGELOG.md",
        "core/agent_roles.md",
        "rules/human_approval.md",
    ]
    for relative in obsolete:
        if (root / relative).exists():
            errors.append(f"obsolete file still present: {relative}")

    check_character_examples(root, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("V0.5.3 package validation passed: character CSVs, complete prompts, screenplay, intake and Vidu direct-only gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
