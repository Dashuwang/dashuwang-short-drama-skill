#!/usr/bin/env python3
"""Validate the lean three-stage AI drama skill package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors: list[str] = []

    required = [
        "SKILL.md",
        "VERSION",
        "PROJECT_KNOWLEDGE_BASE.md",
        "core/workflow.md",
        "references/core-scope-and-acceptance-v0.3.md",
        "modules/asset_analysis/decision_method_v0.2.md",
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
        for phrase in ("小说改编成脚本", "脚本生成符资产提示词", "脚本与符生成视频"):
            if phrase not in content:
                errors.append(f"SKILL.md missing core stage: {phrase}")

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

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Lean package validation passed: three core stages, minimal asset decisions, JSON, and routes are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
