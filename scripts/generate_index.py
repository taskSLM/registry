#!/usr/bin/env python3
"""
SLM World Registry Index Generator

Parses all model, dataset, and task YAML files and produces a single
index.json that provides programmatic access to the entire registry.

Usage:
  python scripts/generate_index.py                    # writes index.json
  python scripts/generate_index.py --output dist.json # custom path
  python scripts/generate_index.py --pretty false     # minified JSON
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent


def load_yaml_files(subdir: str) -> dict[str, dict]:
    """Load all YAML files from a subdirectory. Returns {id: data}."""
    result = {}
    d = ROOT / subdir
    if not d.exists():
        return result
    for fp in sorted(d.glob("*.yaml")):
        if fp.name == ".gitkeep":
            continue
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data and isinstance(data, dict):
                key = fp.stem
                data["_file"] = f"{subdir}/{fp.name}"
                result[key] = data
        except Exception as e:
            print(f"WARNING: Skipping {fp}: {e}", file=sys.stderr)
    return result


def extract_task_cross_references(tasks: dict) -> dict[str, dict]:
    """Extract reverse cross-references: which models/datasets appear in which tasks."""
    cross_ref = defaultdict(lambda: {"models": [], "datasets": []})

    for task_id, task in tasks.items():
        for rec in task.get("recommended_models", []):
            if isinstance(rec, dict) and "ref" in rec:
                # Extract model key from ref path (e.g., "models/phi-4-mini-instruct.yaml" → "phi-4-mini-instruct")
                model_key = Path(rec["ref"]).stem
                entry = {"task": task_id, "notes": rec.get("notes", "")}
                cross_ref[model_key]["models"].append(entry)

        for rec in task.get("recommended_datasets", []):
            if isinstance(rec, dict) and "ref" in rec:
                dataset_key = Path(rec["ref"]).stem
                entry = {
                    "task": task_id,
                    "purpose": rec.get("purpose", ""),
                    "notes": rec.get("notes", "")
                }
                cross_ref[dataset_key]["datasets"].append(entry)

    return dict(cross_ref)


def build_license_summary(models: dict, datasets: dict) -> dict:
    """Count entries by license type."""
    licenses = defaultdict(lambda: {"models": 0, "datasets": 0})
    for m in models.values():
        lic = m.get("license", "Unknown")
        licenses[lic]["models"] += 1
    for d in datasets.values():
        lic = d.get("license", "Unknown")
        licenses[lic]["datasets"] += 1
    return dict(licenses)


def build_param_size_buckets(models: dict) -> dict[str, int]:
    """Count models by parameter size bucket."""
    buckets = {"Under 1B": 0, "1B - 3B": 0, "3B - 5B": 0, "5B - 8B": 0}
    for m in models.values():
        p_str = m.get("parameters", "")
        # Try to extract numeric value
        import re
        match = re.search(r'(\d+\.?\d*)\s*B', str(p_str))
        if match:
            val = float(match.group(1))
            if val < 1:
                buckets["Under 1B"] += 1
            elif val < 3:
                buckets["1B - 3B"] += 1
            elif val < 5:
                buckets["3B - 5B"] += 1
            else:
                buckets["5B - 8B"] += 1
        else:
            # Check for M (millions)
            match = re.search(r'(\d+)\s*M', str(p_str))
            if match:
                val = float(match.group(1)) / 1000
                if val < 1:
                    buckets["Under 1B"] += 1
    return buckets


def build_task_graph(tasks: dict) -> list[dict]:
    """Build task relationship graph for visualization."""
    nodes = []
    edges = []
    task_ids = set(tasks.keys())

    for task_id, task in tasks.items():
        nodes.append({
            "id": task_id,
            "display_name": task.get("display_name", task_id),
            "domain": task.get("domain", ""),
        })
        for rel in task.get("related_tasks", []):
            if isinstance(rel, dict) and rel.get("task_id") in task_ids:
                edges.append({
                    "from": task_id,
                    "to": rel["task_id"],
                    "relationship": rel.get("relationship", "related")
                })

    return {"nodes": nodes, "edges": edges}


def load_benchmarks() -> list[dict]:
    """Load and enrich benchmark entries from benchmarks.yaml."""
    bench_path = ROOT / "benchmarks" / "benchmarks.yaml"
    if not bench_path.exists():
        return []
    with open(bench_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    entries = data.get("entries", []) if data else []

    # Enrich with model names and task display names for frontend rendering
    models = load_yaml_files("models")
    tasks = load_yaml_files("tasks")
    for e in entries:
        model_ref = e.get("model", "").replace("models/", "").replace(".yaml", "")
        task_ref = e.get("task", "").replace("tasks/", "").replace(".yaml", "")
        if model_ref in models:
            e["_model_name"] = models[model_ref].get("name", model_ref)
        if task_ref in tasks:
            e["_task_name"] = tasks[task_ref].get("display_name", task_ref)
    return entries


def generate_index(pretty: bool = True) -> dict:
    """Build the complete registry index."""
    models = load_yaml_files("models")
    datasets = load_yaml_files("datasets")
    tasks = load_yaml_files("tasks")

    cross_refs = extract_task_cross_references(tasks)

    index = {
        "meta": {
            "name": "SLM World Registry",
            "description": "The world's largest registry of Small Language Models under 8B parameters",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "counts": {
                "models": len(models),
                "datasets": len(datasets),
                "tasks": len(tasks),
                "benchmarks": 0,  # populated below
            }
        },
        "models": {},
        "datasets": {},
        "tasks": tasks,
        "cross_references": cross_refs,
        "summaries": {
            "licenses": build_license_summary(models, datasets),
            "param_size_buckets": build_param_size_buckets(models),
        },
        "task_graph": build_task_graph(tasks),
        "benchmarks": [],
    }

    # Load benchmarks
    index["benchmarks"] = load_benchmarks()
    index["meta"]["counts"]["benchmarks"] = len(index["benchmarks"])

    # Add models with their task connections
    for key, model in models.items():
        model_entry = dict(model)
        # Add reverse lookups — which tasks reference this model
        model_entry["_connected_tasks"] = [
            ref["task"] for ref in cross_refs.get(key, {}).get("models", [])
        ]
        index["models"][key] = model_entry

    for key, dataset in datasets.items():
        ds_entry = dict(dataset)
        ds_entry["_connected_tasks"] = [
            ref["task"] for ref in cross_refs.get(key, {}).get("datasets", [])
        ]
        index["datasets"][key] = ds_entry

    return index


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate SLM World registry index.json"
    )
    parser.add_argument(
        "--output", "-o",
        default=str(ROOT / "index.json"),
        help="Output file path (default: index.json in repo root)"
    )
    parser.add_argument(
        "--pretty",
        default=True,
        action="store_true",
        help="Pretty-print JSON (default)"
    )
    parser.add_argument(
        "--no-pretty",
        dest="pretty",
        action="store_false",
        help="Minify JSON output"
    )
    args = parser.parse_args()

    print("Generating SLM World registry index...")
    index = generate_index(pretty=args.pretty)

    output_path = Path(args.output)
    indent = 2 if args.pretty else None

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=indent, ensure_ascii=False)

    print(f"Index written to {output_path}")
    print(f"   Models:    {index['meta']['counts']['models']}")
    print(f"   Datasets:  {index['meta']['counts']['datasets']}")
    print(f"   Tasks:     {index['meta']['counts']['tasks']}")

    # Print license breakdown
    print(f"\nLicense breakdown:")
    for lic, counts in index["summaries"]["licenses"].items():
        parts = []
        if counts["models"]:
            parts.append(f"{counts['models']} models")
        if counts["datasets"]:
            parts.append(f"{counts['datasets']} datasets")
        print(f"   {lic}: {', '.join(parts)}")

    # Parameter size breakdown
    print(f"\nParameter size distribution:")
    for bucket, count in index["summaries"]["param_size_buckets"].items():
        print(f"   {bucket}: {count} models")


if __name__ == "__main__":
    main()
