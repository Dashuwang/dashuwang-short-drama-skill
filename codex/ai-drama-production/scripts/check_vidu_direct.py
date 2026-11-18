#!/usr/bin/env python3
"""Fail closed on incomplete local evidence for a Vidu direct nopeak submission."""

import argparse
import json
from pathlib import Path
import re
import sys


ROUTE_KEYS = ("transport", "model_version", "generation_type", "schedule_mode", "audio_mode")


def mapping(value):
    return value if isinstance(value, dict) else {}


def present(value):
    return isinstance(value, str) and bool(value.strip())


def reasons(record):
    """Validate the local record, not the provider or the truth of its evidence."""
    record = mapping(record)
    route = mapping(record.get("route"))
    output = mapping(record.get("native_audio_output"))
    quote = mapping(record.get("live_zero_cost"))
    issues = []

    if (route.get("transport") not in ("frame_direct", "vidu_cli_direct")
            or route.get("schedule_mode") != "nopeak"
            or route.get("audio_mode") != "native_prompt_audio"
            or any(not present(route.get(key)) for key in ROUTE_KEYS)):
        issues.append("direct_nopeak_route_required")
    if record.get("sound_plan") != "native_audible_audio" or record.get("sound_in_prompt") is not True:
        issues.append("native_sound_plan_required_even_without_dialogue")

    # Input-audio availability is deliberately not read here.
    if output.get("status") != "supported" or not present(output.get("evidence_ref")):
        issues.append("native_audio_output_not_verified")
    if mapping(output.get("route")) != route:
        issues.append("native_audio_evidence_route_mismatch")
    kind = output.get("source")
    if kind == "same_route_original":
        if (not present(output.get("task_id")) or output.get("original_audio_stream") is not True
                or output.get("original_audio_audible") is not True):
            issues.append("prior_original_audio_not_verified")
    elif kind == "explicit_output_capability":
        if output.get("explicitly_confirms_output") is not True:
            issues.append("explicit_output_capability_required")
    else:
        issues.append("audio_input_or_other_evidence_is_insufficient")

    payload_hash = record.get("payload_sha256")
    if (not isinstance(payload_hash, str) or not re.fullmatch(r"[a-f0-9]{64}", payload_hash)
            or quote.get("payload_sha256") != payload_hash):
        issues.append("live_check_payload_mismatch")
    if (mapping(quote.get("route")) != route or quote.get("valid_now") is not True
            or not present(quote.get("evidence_ref"))):
        issues.append("live_nopeak_check_missing_or_expired")
    cost = quote.get("cost_credits")
    remaining = quote.get("remaining")
    if type(cost) is not int or cost != 0:
        issues.append("exact_zero_credits_required")
    if type(remaining) is not int or remaining <= 0:
        issues.append("positive_nopeak_quota_required")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, ValueError):
        issues = ["invalid_preflight_record"]
    else:
        issues = reasons(record)
    print(json.dumps({"preflight_passed": not issues, "issues": issues}))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
