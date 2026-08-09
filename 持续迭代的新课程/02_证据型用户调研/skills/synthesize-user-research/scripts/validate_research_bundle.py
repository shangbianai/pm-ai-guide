#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_research_bundle.py research-bundle.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR invalid JSON: {exc}")
        return 1

    errors, warnings = [], []
    required = ["meta", "sources", "evidence", "contradictions", "findings", "persona", "journey", "opportunities", "next_questions"]
    for key in required:
        if key not in data:
            errors.append(f"missing top-level field: {key}")

    sources = data.get("sources", [])
    source_ids = [x.get("id") for x in sources]
    if not sources:
        errors.append("sources must not be empty")
    if len(source_ids) != len(set(source_ids)):
        errors.append("source IDs must be unique")

    evidence = data.get("evidence", [])
    evidence_ids = [x.get("id") for x in evidence]
    if not evidence:
        errors.append("evidence must not be empty")
    if len(evidence_ids) != len(set(evidence_ids)):
        errors.append("evidence IDs must be unique")
    for item in evidence:
        if item.get("source_id") not in source_ids:
            errors.append(f"{item.get('id')}: unknown source_id {item.get('source_id')}")
        if not item.get("locator") or not item.get("content"):
            errors.append(f"{item.get('id')}: locator and content are required")

    def check_refs(label, item, require=True):
        refs = item.get("evidence_ids", [])
        if require and not refs:
            errors.append(f"{label}: evidence_ids required")
        for ref in refs:
            if ref not in evidence_ids:
                errors.append(f"{label}: unknown evidence id {ref}")

    for item in data.get("findings", []):
        status = item.get("status")
        check_refs(item.get("id", "finding"), item, status != "待验证假设")
        if status == "待验证假设" and not item.get("validation"):
            errors.append(f"{item.get('id')}: hypothesis requires validation plan")

    claims = data.get("persona", {}).get("claims", [])
    if not claims:
        errors.append("persona.claims must not be empty")
    for index, item in enumerate(claims, 1):
        check_refs(f"persona claim {index}", item)

    journey = data.get("journey", [])
    if not 5 <= len(journey) <= 7:
        errors.append("journey must contain 5 to 7 stages")
    for index, item in enumerate(journey, 1):
        emotion = item.get("emotion")
        if not isinstance(emotion, int) or not -2 <= emotion <= 2:
            errors.append(f"journey stage {index}: emotion must be integer -2..2")
        check_refs(f"journey stage {index}", item, item.get("status") != "待验证假设")

    opportunities = data.get("opportunities", [])
    if len(opportunities) < 3:
        errors.append("at least 3 opportunities are required")
    ranks = []
    for index, item in enumerate(opportunities, 1):
        ranks.append(item.get("rank"))
        check_refs(f"opportunity {index}", item)
        for field in ("impact", "frequency", "risk"):
            value = item.get(field)
            if not isinstance(value, int) or not 1 <= value <= 5:
                errors.append(f"opportunity {index}: {field} must be integer 1..5")
    if ranks and ranks != sorted(ranks):
        warnings.append("opportunities are not ordered by rank")

    if len(data.get("next_questions", [])) < 5:
        errors.append("at least 5 next_questions are required")
    if len(data.get("meta", {}).get("limitations", [])) == 0:
        warnings.append("meta.limitations is empty")

    sync = data.get("feishu_sync")
    if sync and sync.get("requested"):
        if sync.get("numbered_h1") is not True:
            errors.append("feishu_sync numbered_h1 must be true")
        if sync.get("evidence_display") != "id+description+source+locator":
            errors.append("feishu_sync evidence_display must be id+description+source+locator")
        transcript = sync.get("transcript", {})
        if transcript.get("source_id") not in source_ids:
            errors.append("feishu_sync transcript has unknown source_id")
        if transcript.get("mode") != "inline_text":
            errors.append("feishu_sync transcript mode must be inline_text")
        transcript_path = path.parent / transcript.get("local_path", "")
        if not transcript.get("local_path") or not transcript_path.is_file():
            errors.append("feishu_sync transcript local_path is missing or unreadable")

        media = sync.get("media", [])
        if not media:
            errors.append("feishu_sync media must not be empty")
        audio_count = 0
        synced_image_sources = set()
        for index, item in enumerate(media, 1):
            label = f"feishu_sync media {index}"
            if item.get("source_id") not in source_ids:
                errors.append(f"{label}: unknown source_id")
            # Some uploaded originals (for example a material README or a duplicate
            # audio encoding) are part of the audit trail without introducing new
            # evidence. They still need a valid source_id and a real local file.
            check_refs(label, item, False)
            media_path = path.parent / item.get("local_path", "")
            if not item.get("local_path") or not media_path.is_file():
                errors.append(f"{label}: local_path is missing or unreadable")
            if item.get("media_type") == "audio":
                audio_count += 1
                if item.get("mode") != "attachment":
                    errors.append(f"{label}: audio mode must be attachment")
            if item.get("media_type") == "image":
                synced_image_sources.add(item.get("source_id"))
                if item.get("mode") != "embed":
                    errors.append(f"{label}: image mode must be embed")
                caption = item.get("caption", "")
                if item.get("source_id", "") not in caption or not any(ref in caption for ref in item.get("evidence_ids", [])):
                    errors.append(f"{label}: image caption must include source_id and an evidence id")
        if audio_count == 0:
            errors.append("feishu_sync requires at least one audio attachment")
        expected_images = {x.get("id") for x in sources if x.get("type") == "image" and x.get("status") == "已读取"}
        missing_images = expected_images - synced_image_sources
        if missing_images:
            errors.append(f"feishu_sync missing readable image sources: {', '.join(sorted(missing_images))}")
        if sync.get("upload_all_sources"):
            synced_sources = {x.get("source_id") for x in media}
            expected_sources = {x.get("id") for x in sources if x.get("status") == "已读取"}
            missing_sources = expected_sources - synced_sources
            if missing_sources:
                errors.append(f"feishu_sync missing input file uploads: {', '.join(sorted(missing_sources))}")
            table = sync.get("materials_table", {})
            if table.get("enabled") is not True:
                errors.append("feishu_sync materials_table must be enabled")
            rows = table.get("rows", [])
            row_sources = {x.get("source_id") for x in rows}
            missing_rows = expected_sources - row_sources
            if missing_rows:
                errors.append(f"feishu_sync materials table missing sources: {', '.join(sorted(missing_rows))}")
            for index, row in enumerate(rows, 1):
                if row.get("source_id") not in source_ids:
                    errors.append(f"materials table row {index}: unknown source_id")
                if not row.get("summary") or not row.get("presentation") or not row.get("file_name"):
                    errors.append(f"materials table row {index}: file_name, summary and presentation are required")
                check_refs(f"materials table row {index}", row, False)

    for warning in warnings:
        print(f"WARNING {warning}")
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print(f"FAILED {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    sync_note = " with Feishu media plan" if sync and sync.get("requested") else ""
    print(f"PASS {len(sources)} sources, {len(evidence)} evidence items, {len(journey)} journey stages, {len(opportunities)} opportunities{sync_note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
