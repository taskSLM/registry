#!/usr/bin/env python3
"""
SLM World Registry Validator

Validates all YAML files in the registry for:
  - Valid YAML syntax
  - Required fields per schema (model, dataset, task)
  - HuggingFace URL reachability
  - Cross-reference integrity (task refs → actual files)
  - Parameter format conformance
  - Known tag vocabulary (warns on unknown)
  - Duplicate detection

Usage:
  python scripts/validate.py                  # validate everything
  python scripts/validate.py models/foo.yaml  # validate one file
  python scripts/validate.py --check-refs     # also check cross-references
  python scripts/validate.py --strict         # fail on tag warnings too
"""

import sys
import os
import re
import json
import urllib.request
import urllib.error
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

# ── Schema Definitions ──────────────────────────────────────────────

MODEL_REQUIRED = [
    "name", "developer", "parameters", "primary_task",
    "context_window", "license", "huggingface_url", "description"
]
MODEL_OPTIONAL = ["tags", "submitted_by", "predecessor", "successor",
                   "generation", "family", "param_count_m", "param_total_m",
                   "badges", "hardware_compat"]

DATASET_REQUIRED = [
    "name", "creator", "size_rows", "target_task",
    "license", "huggingface_url", "description"
]
DATASET_OPTIONAL = ["tags", "notes"]

TASK_REQUIRED = [
    "task_id", "display_name", "description",
    "input_format", "output_format", "metrics_tracked"
]
TASK_OPTIONAL = [
    "domain", "difficulty", "recommended_models",
    "recommended_datasets", "related_tasks", "tags",
    "prompt_template", "evaluation", "hardware_requirements",
    "deployment_guidance", "community"
]

VALID_RELATIONSHIPS = {"parent", "child", "related", "enhances"}

# ── Known Tag Vocabulary ────────────────────────────────────────────

KNOWN_TAGS = {
    # Capability
    "reasoning", "code-generation", "math-reasoning", "multilingual",
    "multimodal", "vision", "audio", "video", "tool-calling",
    "function-calling", "agentic", "chat", "instruction-following",
    "knowledge-qa", "text-to-sql", "summarization", "translation",
    "named-entity-recognition", "sentiment-analysis",
    # Deployment
    "edge-computing", "on-device", "mobile", "lightweight",
    "efficient", "production", "local-llm",
    # Quality / Openness
    "open-source", "fully-open", "reproducible", "research",
    "community", "benchmark", "baseline",
    # Data characteristics
    "fine-tuning", "evaluation", "synthetic-data", "large-scale",
    "chain-of-thought", "decontaminated", "multi-table", "complex-sql",
    "multi-language", "structured-output", "structured-data",
    # Alignment
    "alignment", "dpo", "rlhf", "safety", "post-training",
    "preference-tuning",
    # Misc
    "long-context", "thinking-mode", "high-performance",
    # Deployment (extended)
    "tiny", "enterprise",
    # Capability (extended)
    "tool-use", "open-science", "rag", "code",
    # Data processing
    "instruction-tuning", "programming", "general-purpose",
}


def warn(msg: str) -> None:
    print(f"  [!] WARNING: {msg}")

def error(msg: str) -> None:
    print(f"  [X] ERROR: {msg}")

def ok(msg: str) -> None:
    print(f"  [+] {msg}")


# ── Checkers ────────────────────────────────────────────────────────

def validate_yaml_syntax(filepath: Path) -> dict | None:
    """Parse YAML, return data or None on failure."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data is None:
            error(f"File is empty or only contains comments")
            return None
        if not isinstance(data, dict):
            error(f"Expected a YAML mapping, got {type(data).__name__}")
            return None
        return data
    except yaml.YAMLError as e:
        error(f"YAML parse error: {e}")
        return None
    except Exception as e:
        error(f"Could not read file: {e}")
        return None


def get_schema_type(filepath: Path) -> str:
    """Determine schema type from parent directory name."""
    parent = filepath.parent.name
    if parent == "models":
        return "model"
    elif parent == "datasets":
        return "dataset"
    elif parent == "tasks":
        return "task"
    return "unknown"


def validate_required_fields(data: dict, schema_type: str) -> list[str]:
    """Check all required fields are present. Returns list of missing fields."""
    if schema_type == "model":
        required = MODEL_REQUIRED
    elif schema_type == "dataset":
        required = DATASET_REQUIRED
    elif schema_type == "task":
        required = TASK_REQUIRED
    else:
        return []

    missing = [f for f in required if f not in data or data[f] is None]
    return missing


def validate_field_types(data: dict, schema_type: str) -> list[str]:
    """Check field types are reasonable. Returns list of issues."""
    issues = []

    if schema_type == "task":
        if "metrics_tracked" in data:
            if not isinstance(data["metrics_tracked"], list):
                issues.append("metrics_tracked must be a list")
        if "recommended_models" in data and isinstance(data["recommended_models"], list):
            for i, entry in enumerate(data["recommended_models"]):
                if not isinstance(entry, dict) or "ref" not in entry:
                    issues.append(f"recommended_models[{i}] must have a 'ref' field")
        if "recommended_datasets" in data and isinstance(data["recommended_datasets"], list):
            for i, entry in enumerate(data["recommended_datasets"]):
                if not isinstance(entry, dict) or "ref" not in entry:
                    issues.append(f"recommended_datasets[{i}] must have a 'ref' field")
        if "related_tasks" in data and isinstance(data["related_tasks"], list):
            for i, entry in enumerate(data["related_tasks"]):
                if not isinstance(entry, dict):
                    issues.append(f"related_tasks[{i}] must be a mapping")
                elif "task_id" not in entry:
                    issues.append(f"related_tasks[{i}] missing 'task_id'")
                elif "relationship" in entry and entry["relationship"] not in VALID_RELATIONSHIPS:
                    issues.append(
                        f"related_tasks[{i}]: '{entry['relationship']}' not in {VALID_RELATIONSHIPS}"
                    )

    if "tags" in data:
        if not isinstance(data["tags"], list):
            issues.append("tags must be a list")

    return issues


def validate_tags(data: dict, strict: bool = False) -> list[str]:
    """Check tags against known vocabulary. Returns warnings."""
    warnings_list = []
    if "tags" not in data:
        return warnings_list
    tags = data["tags"]
    if not isinstance(tags, list):
        return warnings_list
    for tag in tags:
        if tag not in KNOWN_TAGS:
            msg = f"Unknown tag: '{tag}' (consider adding to TAGS.md or using a known tag)"
            warnings_list.append(msg)
    return warnings_list


def validate_parameter_format(data: dict, schema_type: str) -> list[str]:
    """Check parameter field format for models."""
    if schema_type != "model":
        return []
    if "parameters" not in data:
        return []
    p = str(data["parameters"])
    if not re.search(r'\d+\.?\d*\s*[BM]', p):
        return [f"Parameters field may not be in standard format: '{p}'"]
    return []


def check_url(url: str, timeout: int = 10) -> tuple[bool, str]:
    """Check if a URL is reachable. Returns (ok, message)."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "slm-world-validator/1.0")
        resp = urllib.request.urlopen(req, timeout=timeout)
        return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, f"Unreachable: {e.reason}"
    except Exception as e:
        return False, f"Error: {e}"


def validate_cross_references(data: dict, schema_type: str) -> list[str]:
    """Check that refs in task YAMLs point to real files."""
    issues = []
    if schema_type != "task":
        return issues

    for field, subdir in [("recommended_models", "models"),
                           ("recommended_datasets", "datasets")]:
        if field not in data:
            continue
        if not isinstance(data[field], list):
            continue
        for i, entry in enumerate(data[field]):
            if not isinstance(entry, dict) or "ref" not in entry:
                continue
            ref_path = ROOT / entry["ref"]
            if not ref_path.exists():
                issues.append(
                    f"{field}[{i}]: ref '{entry['ref']}' does not exist"
                )

    # Check related_tasks
    if "related_tasks" in data and isinstance(data["related_tasks"], list):
        for i, entry in enumerate(data["related_tasks"]):
            if not isinstance(entry, dict) or "task_id" not in entry:
                continue
            ref_path = ROOT / "tasks" / f"{entry['task_id']}.yaml"
            if not ref_path.exists() and entry["task_id"] != data.get("task_id"):
                issues.append(
                    f"related_tasks[{i}]: task '{entry['task_id']}' not found "
                    f"(expected {ref_path.name})"
                )

    return issues


def find_duplicates(all_files: list[Path]) -> dict[str, list[Path]]:
    """Detect files that appear to represent the same entity."""
    seen_names = defaultdict(list)
    for fp in all_files:
        key = fp.stem.lower()
        seen_names[key].append(fp)
    return {k: v for k, v in seen_names.items() if len(v) > 1}


# ── Main ────────────────────────────────────────────────────────────

def validate_file(filepath: Path, strict: bool = False,
                  check_urls: bool = False, check_refs: bool = False) -> int:
    """Validate a single YAML file. Returns count of errors."""
    rel = filepath.relative_to(ROOT)
    print(f"\n{'---'*20}")
    print(f"  File: {rel}")
    print(f"{'---'*20}")

    errors = 0
    warnings_count = 0
    schema_type = get_schema_type(filepath)

    if schema_type == "unknown":
        error(f"Cannot determine schema type — file should be in models/, datasets/, or tasks/")
        return 1

    # 1. Parse YAML
    data = validate_yaml_syntax(filepath)
    if data is None:
        return 1

    # 2. Required fields
    missing = validate_required_fields(data, schema_type)
    if missing:
        for m in missing:
            error(f"Missing required field: '{m}'")
        errors += len(missing)
    else:
        ok("All required fields present")

    # 3. Field types
    type_issues = validate_field_types(data, schema_type)
    for issue in type_issues:
        error(issue)
    errors += len(type_issues)

    # 4. Parameter format (models only)
    param_issues = validate_parameter_format(data, schema_type)
    for issue in param_issues:
        warn(issue)
    warnings_count += len(param_issues)

    # 5. Tags
    tag_issues = validate_tags(data, strict)
    for issue in tag_issues:
        if strict:
            error(issue)
            errors += 1
        else:
            warn(issue)
            warnings_count += 1

    # 6. URL check
    if check_urls and "huggingface_url" in data:
        url = data["huggingface_url"]
        is_ok, msg = check_url(url)
        if is_ok:
            ok(f"URL reachable: {url} ({msg})")
        else:
            error(f"URL check failed: {url} ({msg})")
            errors += 1

    # 7. Cross-references
    if check_refs:
        ref_issues = validate_cross_references(data, schema_type)
        for issue in ref_issues:
            error(issue)
        errors += len(ref_issues)
        if not ref_issues:
            ok("All cross-references valid")

    status = "[FAIL]" if errors > 0 else "[PASS]"
    summary = f"{status}"
    if warnings_count > 0:
        summary += f" ({warnings_count} warning(s))"
    print(f"\n  -> {summary}")
    return errors


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate SLM World registry YAML files")
    parser.add_argument("files", nargs="*", help="Specific YAML files to validate")
    parser.add_argument("--check-urls", action="store_true",
                        help="Check that HuggingFace URLs are reachable")
    parser.add_argument("--check-refs", action="store_true",
                        help="Validate cross-references between files")
    parser.add_argument("--strict", action="store_true",
                        help="Treat unknown tags as errors")
    args = parser.parse_args()

    # Collect files
    if args.files:
        files = [Path(f).resolve() for f in args.files]
        for fp in files:
            if not fp.exists():
                print(f"ERROR: File not found: {fp}")
                sys.exit(1)
    else:
        files = []
        for subdir in ["models", "datasets", "tasks"]:
            d = ROOT / subdir
            if d.exists():
                files.extend(sorted(d.glob("*.yaml")))
        # Exclude .gitkeep
        files = [f for f in files if f.name != ".gitkeep"]

    if not files:
        print("No YAML files found to validate.")
        sys.exit(0)

    print(f"\nSLM World Registry Validator")
    print(f"   Validating {len(files)} file(s)")
    if args.check_urls:
        print(f"   URL checking: ON")
    if args.check_refs:
        print(f"   Cross-reference checking: ON")

    total_errors = 0
    for fp in files:
        total_errors += validate_file(fp, strict=args.strict,
                                       check_urls=args.check_urls,
                                       check_refs=args.check_refs)

    # Duplicate detection
    duplicates = find_duplicates(files)
    if duplicates:
        print(f"\n{'---'*20}")
        print("Duplicate Detection")
        print(f"{'---'*20}")
        for name, paths in duplicates.items():
            error(f"Duplicate files for '{name}': {[str(p.relative_to(ROOT)) for p in paths]}")
            total_errors += 1

    print(f"\n{'==='*20}")
    if total_errors == 0:
        print(f"All {len(files)} file(s) validated successfully!")
        sys.exit(0)
    else:
        print(f"Validation failed with {total_errors} error(s)")
        sys.exit(1)


if __name__ == "__main__":
    main()
