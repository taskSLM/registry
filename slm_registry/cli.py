"""
CLI for the SLM World Registry.

Usage:
  slm list models              List all models
  slm list datasets            List all datasets
  slm list tasks               List all tasks
  slm search <query>           Search models and datasets
  slm info <name>              Show detailed model info
  slm task <task-id>           Show task with recommended models & datasets
  slm compare <m1> <m2>        Compare two models side-by-side
  slm hardware [target]        Show hardware compatibility matrix
  slm stats                    Show registry statistics
"""

import sys
from pathlib import Path

from .registry import (
    load_index, get_models, get_datasets, get_tasks,
    search_models, search_datasets, get_model_by_name,
    get_task_by_id, filter_models_by_hardware, get_stats,
)
from . import __version__

# ASCII-safe formatting
_SEP = "-" * 60


def _param_sort_key(model: dict) -> float:
    """Extract numeric parameter count for sorting."""
    import re
    p = model.get("parameters", "0")
    match = re.search(r"(\d+\.?\d*)\s*B", str(p))
    if match:
        return float(match.group(1))
    match = re.search(r"(\d+)\s*M", str(p))
    if match:
        return float(match.group(1)) / 1000
    return 0.0


def _yes_no(value: bool) -> str:
    return "YES" if value else " no"


def _model_header(name: str) -> str:
    """Emphasize model names with asterisks since ANSI may not work on Windows."""
    return f"*{name}*"


# --- Commands ---

def cmd_list(index: dict, what: str) -> None:
    """List models, datasets, or tasks."""
    if what == "models":
        models = sorted(get_models(index).items(),
                        key=lambda x: _param_sort_key(x[1]), reverse=True)
        print(f"\nModels ({len(models)} total)\n")
        print(f"  {'Name':<35} {'Params':<12} {'License':<28} {'Best For'}")
        print(f"  {'-'*35} {'-'*12} {'-'*28} {'-'*30}")
        for key, m in models:
            name = m.get("name", key)[:33]
            params = m.get("parameters", "?")
            license_ = m.get("license", "?")[:26]
            task = m.get("primary_task", "?")[:28]
            print(f"  {name:<35} {params:<12} {license_:<28} {task}")

    elif what == "datasets":
        datasets = sorted(get_datasets(index).items(),
                          key=lambda x: x[1].get("name", ""))
        print(f"\nDatasets ({len(datasets)} total)\n")
        print(f"  {'Name':<40} {'Rows':<14} {'License':<22} {'Target Task'}")
        print(f"  {'-'*40} {'-'*14} {'-'*22} {'-'*30}")
        for key, d in datasets:
            name = d.get("name", key)[:38]
            rows = d.get("size_rows", "?")[:12]
            license_ = d.get("license", "?")[:20]
            task = d.get("target_task", "?")[:28]
            print(f"  {name:<40} {rows:<14} {license_:<22} {task}")

    elif what == "tasks":
        tasks = sorted(get_tasks(index).items(),
                       key=lambda x: x[1].get("display_name", ""))
        print(f"\nTasks ({len(tasks)} total)\n")
        for key, t in tasks:
            display = t.get("display_name", key)
            domain = t.get("domain", "")
            n_models = len(t.get("recommended_models", []))
            n_datasets = len(t.get("recommended_datasets", []))
            print(f"  {display}")
            print(f"    {domain}  |  {n_models} models, {n_datasets} datasets")
            desc = t.get("description", "")[:120]
            print(f"    {desc}...")
            print()

    else:
        print(f"Unknown list target: {what}. Use: models, datasets, or tasks.")
        sys.exit(1)


def cmd_search(index: dict, query: str) -> None:
    """Search across models and datasets."""
    print(f"\nSearch results for: {query}\n")

    models = search_models(index, query)
    datasets = search_datasets(index, query)

    if models:
        print(f"  Models ({len(models)} found):")
        for key, m in models[:10]:
            params = m.get("parameters", "?")
            task = m.get("primary_task", "")
            dev = m.get("developer", "")
            print(f"    {_model_header(m.get('name', key))}  {params}  {dev}")
            print(f"      {task}")
        if len(models) > 10:
            print(f"    ... and {len(models) - 10} more. Narrow your search.")
        print()

    if datasets:
        print(f"  Datasets ({len(datasets)} found):")
        for key, d in datasets[:5]:
            rows = d.get("size_rows", "?")
            task = d.get("target_task", "")
            print(f"    {_model_header(d.get('name', key))}  {rows} rows")
            print(f"      {task}")
        if len(datasets) > 5:
            print(f"    ... and {len(datasets) - 5} more. Narrow your search.")
        print()

    if not models and not datasets:
        print(f"  No results found for '{query}'. Try a different search term.")


def cmd_info(index: dict, name: str) -> None:
    """Show detailed info for a model."""
    model = get_model_by_name(index, name)
    if model is None:
        print(f"Model not found: {name}")
        sys.exit(1)

    print(f"\n  {_model_header(model.get('name', name))}")
    print(f"  {_SEP}")
    print(f"  Developer:      {model.get('developer', '?')}")
    print(f"  Parameters:     {model.get('parameters', '?')}")
    print(f"  Context Window: {model.get('context_window', '?')}")
    print(f"  License:        {model.get('license', '?')}")
    print(f"  Primary Task:   {model.get('primary_task', '?')}")
    print(f"  HF URL:         {model.get('huggingface_url', '?')}")
    print()

    hw = model.get("hardware_compat", {})
    if hw:
        print(f"  Hardware Compatibility:")
        print(f"    Raspberry Pi 5:     {_yes_no(hw.get('raspberry_pi_5', False))}")
        print(f"    Mobile Phone:       {_yes_no(hw.get('mobile_phone', False))}")
        print(f"    GPU (8 GB VRAM):    {_yes_no(hw.get('consumer_gpu_8gb', False))}")
        print(f"    GPU (24 GB VRAM):   {_yes_no(hw.get('consumer_gpu_24gb', False))}")
        print(f"    CPU Only:           {_yes_no(hw.get('cpu_only', False))}")
        print(f"    Apple Silicon 16GB: {_yes_no(hw.get('apple_silicon_16gb', False))}")
        if hw.get("min_ram_gb_q4"):
            print(f"    Min RAM (Q4 quant): {hw['min_ram_gb_q4']} GB")
        if hw.get("recommended_backend"):
            print(f"    Recommended Backend: {hw['recommended_backend']}")
    print()

    tasks = model.get("_connected_tasks", [])
    if tasks:
        print(f"  Connected Tasks: {', '.join(t for t in tasks)}")
        print()

    tags = model.get("tags", [])
    if tags:
        print(f"  Tags: {', '.join(tags)}")
        print()

    print(f"  Description:")
    print(f"  {model.get('description', 'No description available.')}")
    print()


def cmd_task(index: dict, task_id: str) -> None:
    """Show task details with recommended models and datasets."""
    task = get_task_by_id(index, task_id)
    if task is None:
        print(f"Task not found: {task_id}")
        sys.exit(1)

    print(f"\n  {task.get('display_name', task_id)}")
    if task.get("domain"):
        print(f"  {task['domain']}")
    print(f"  {_SEP}")
    print(f"  {task.get('description', '')}")
    print()
    print(f"  Input:  {task.get('input_format', '?')}")
    print(f"  Output: {task.get('output_format', '?')}")
    print()

    metrics = task.get("metrics_tracked", [])
    if metrics:
        print(f"  Metrics: {', '.join(metrics)}")
        print()

    rec_models = task.get("recommended_models", [])
    if rec_models:
        print(f"  Recommended Models:")
        for rm in rec_models:
            ref = rm.get("ref", "?")
            notes = rm.get("notes", "")
            print(f"    {ref}")
            if notes:
                print(f"      {notes}")
        print()

    rec_datasets = task.get("recommended_datasets", [])
    if rec_datasets:
        print(f"  Recommended Datasets:")
        for rd in rec_datasets:
            ref = rd.get("ref", "?")
            purpose = rd.get("purpose", "")
            notes = rd.get("notes", "")
            suffix = f" ({purpose})" if purpose else ""
            print(f"    {ref}{suffix}")
            if notes:
                print(f"      {notes}")
        print()

    related = task.get("related_tasks", [])
    if related:
        print(f"  Related Tasks:")
        for rt in related:
            tid = rt.get("task_id", "?")
            rel = rt.get("relationship", "related")
            print(f"    {tid} ({rel})")
        print()


def cmd_compare(index: dict, name1: str, name2: str) -> None:
    """Compare two models side-by-side."""
    m1 = get_model_by_name(index, name1)
    m2 = get_model_by_name(index, name2)

    if m1 is None:
        print(f"Model not found: {name1}")
        sys.exit(1)
    if m2 is None:
        print(f"Model not found: {name2}")
        sys.exit(1)

    n1 = m1.get('name', name1)
    n2 = m2.get('name', name2)
    print(f"\n  Comparison: {n1}  vs  {n2}")
    print(f"  {_SEP}\n")

    rows = [
        ("Developer", "developer"),
        ("Parameters", "parameters"),
        ("Context Window", "context_window"),
        ("License", "license"),
        ("Primary Task", "primary_task"),
    ]

    for label, field in rows:
        v1 = m1.get(field, "?")
        v2 = m2.get(field, "?")
        print(f"  {label:<20} {v1:<25} {v2}")

    hw1 = m1.get("hardware_compat", {})
    hw2 = m2.get("hardware_compat", {})
    if hw1 or hw2:
        print(f"\n  Hardware Compatibility:")
        for hw_key, hw_label in [
            ("raspberry_pi_5", "Raspberry Pi 5"),
            ("mobile_phone", "Mobile Phone"),
            ("consumer_gpu_8gb", "GPU 8 GB VRAM"),
            ("consumer_gpu_24gb", "GPU 24 GB VRAM"),
            ("cpu_only", "CPU Only"),
            ("apple_silicon_16gb", "Apple Silicon 16GB"),
        ]:
            v1 = _yes_no(hw1.get(hw_key, False))
            v2 = _yes_no(hw2.get(hw_key, False))
            print(f"  {hw_label:<20} {v1:<25} {v2}")

        q1 = hw1.get("min_ram_gb_q4", "?")
        q2 = hw2.get("min_ram_gb_q4", "?")
        print(f"  {'Min RAM (Q4)':<20} {str(q1) + ' GB':<25} {str(q2) + ' GB'}")

    print()


def cmd_hardware(index: dict, target: str = "") -> None:
    """Show hardware compatibility matrix."""
    models = sorted(get_models(index).items(),
                    key=lambda x: _param_sort_key(x[1]))

    targets = {
        "rpi": ("raspberry_pi_5", "Raspberry Pi 5"),
        "mobile": ("mobile_phone", "Mobile Phone"),
        "gpu8": ("consumer_gpu_8gb", "GPU 8 GB VRAM"),
        "gpu24": ("consumer_gpu_24gb", "GPU 24 GB VRAM"),
        "cpu": ("cpu_only", "CPU Only"),
        "apple": ("apple_silicon_16gb", "Apple Silicon"),
    }

    if target and target.lower() in targets:
        hw_key, hw_label = targets[target.lower()]
        print(f"\nModels compatible with: {hw_label}\n")
        for key, m in models:
            hw = m.get("hardware_compat", {})
            if hw.get(hw_key, False):
                params = m.get("parameters", "?")
                q4 = hw.get("min_ram_gb_q4", "?")
                print(f"  {_model_header(m.get('name', key)):<42} {params:<10} Q4 RAM: {q4} GB")
        print()
        return

    # Full matrix
    print(f"\nHardware Compatibility Matrix\n")
    header = f"  {'Model':<36} {'Params':<8} {'RPi5':<6} {'Mobile':<8} {'GPU8':<6} {'GPU24':<6} {'CPU':<6} {'Q4 RAM'}"
    print(header)
    print(f"  {'-'*36} {'-'*8} {'-'*6} {'-'*8} {'-'*6} {'-'*6} {'-'*6} {'-'*7}")

    for key, m in models:
        name = m.get("name", key)[:34]
        params = m.get("parameters", "?")[:6]
        hw = m.get("hardware_compat", {})
        rpi = " OK " if hw.get("raspberry_pi_5") else " -- "
        mob = " OK " if hw.get("mobile_phone") else " -- "
        g8 = " OK " if hw.get("consumer_gpu_8gb") else " -- "
        g24 = " OK " if hw.get("consumer_gpu_24gb") else " -- "
        cpu = " OK " if hw.get("cpu_only") else " -- "
        q4 = hw.get("min_ram_gb_q4", "?")
        print(f"  {name:<36} {params:<8} {rpi:<6} {mob:<8} {g8:<6} {g24:<6} {cpu:<6} {q4} GB")

    print()
    print(f"  Use 'slm hardware <target>' to filter by platform.")
    print(f"  Targets: rpi, mobile, gpu8, gpu24, cpu, apple\n")


def cmd_stats(index: dict) -> None:
    """Show registry statistics."""
    stats = get_stats(index)

    print(f"\nSLM World Registry Statistics")
    print(f"{_SEP}\n")
    print(f"  Models:    {stats['models']}")
    print(f"  Datasets:  {stats['datasets']}")
    print(f"  Tasks:     {stats['tasks']}")
    print()

    print(f"  By License:")
    for lic, counts in sorted(stats.get("licenses", {}).items()):
        parts = []
        if counts.get("models", 0):
            parts.append(f"{counts['models']} models")
        if counts.get("datasets", 0):
            parts.append(f"{counts['datasets']} datasets")
        print(f"    {lic}: {', '.join(parts)}")

    print(f"\n  By Parameter Size:")
    for bucket, count in stats.get("param_buckets", {}).items():
        bar = "#" * count
        print(f"    {bucket:<15} {count} {bar}")

    print(f"\n  Hardware Compatibility:")
    hw = stats.get("hardware_compat", {})
    print(f"    Raspberry Pi 5:      {hw.get('raspberry_pi_5', 0)}/{stats['models']} models")
    print(f"    Mobile Phone:        {hw.get('mobile_phone', 0)}/{stats['models']} models")
    print(f"    GPU (8 GB):          {hw.get('consumer_gpu_8gb', 0)}/{stats['models']} models")
    print(f"    CPU Only:            {hw.get('cpu_only', 0)}/{stats['models']} models")
    print()


def cmd_leaderboard(index: dict) -> None:
    """Show benchmark leaderboard from benchmarks.yaml."""
    import yaml
    try:
        import yaml as _yaml
    except ImportError:
        print("PyYAML required for leaderboard. Install with: pip install pyyaml")
        return

    bench_path = Path(__file__).resolve().parent.parent / "benchmarks" / "benchmarks.yaml"
    if not bench_path.exists():
        print("benchmarks/benchmarks.yaml not found.")
        return

    with open(bench_path, "r", encoding="utf-8") as f:
        bench_data = _yaml.safe_load(f)

    entries = bench_data.get("entries", [])
    if not entries:
        print("No benchmark entries found.")
        return

    # Group by task
    from collections import defaultdict
    by_task = defaultdict(list)
    for e in entries:
        task_id = e.get("task", "").replace("tasks/", "").replace(".yaml", "")
        by_task[task_id].append(e)

    print(f"\nBenchmark Leaderboard")
    print(f"{_SEP}\n")

    for task_id, task_entries in sorted(by_task.items()):
        task = index.get("tasks", {}).get(task_id, {})
        display = task.get("display_name", task_id)
        print(f"  {_model_header(display)}")
        print(f"  {'-'*50}")

        # Sort by score descending (assuming higher is better)
        task_entries.sort(key=lambda x: x.get("score", 0), reverse=True)

        for i, e in enumerate(task_entries):
            model_key = e.get("model", "").replace("models/", "").replace(".yaml", "")
            model = index.get("models", {}).get(model_key, {})
            model_name = model.get("name", model_key) if model else model_key
            score = e.get("score", "?")
            metric = e.get("metric", "?")
            verified = " [v]" if e.get("verified") else " [~]"
            prefix = "1st" if i == 0 else f"{i+1}th" if i < 4 else f"{i+1}th"
            print(f"    {prefix} {model_name}: {score} ({metric}){verified}")
            if e.get("notes"):
                print(f"        {e['notes'][:100]}")
        print()

    print(f"  [v] = maintainer-verified  [~] = community-reported, unverified\n")


# --- Main ---

USAGE = f"""
SLM World Registry CLI v{__version__}

Usage:
  slm list models|datasets|tasks     List entries
  slm search <query>                 Search across the registry
  slm info <model-name>              Show model details
  slm task <task-id>                 Show task + recommendations
  slm compare <model1> <model2>      Compare two models
  slm hardware [target]              Hardware compatibility matrix
  slm leaderboard                    Benchmark leaderboard
  slm stats                          Registry statistics
  slm --help                         Show this help

Examples:
  slm list models
  slm search "code generation"
  slm info phi-4-mini
  slm task text-to-sql
  slm compare gemma-3-4b phi-4-mini
  slm hardware mobile
  slm stats

Data source: https://github.com/taskSLM/registry
"""


def main(args: list[str] | None = None) -> None:
    if args is None:
        args = sys.argv[1:]

    if not args or args[0] in ("--help", "-h", "help"):
        print(USAGE)
        sys.exit(1)

    cmd = args[0].lower()

    try:
        index = load_index()
    except Exception as e:
        print(f"Error loading registry index: {e}")
        print(f"Make sure you're online or have a local index.json.")
        print(f"Run from the repo root for local access.")
        sys.exit(1)

    try:
        if cmd == "list":
            what = args[1] if len(args) > 1 else "models"
            cmd_list(index, what)
        elif cmd == "search":
            if len(args) < 2:
                print("Usage: slm search <query>")
                sys.exit(1)
            cmd_search(index, " ".join(args[1:]))
        elif cmd == "info":
            if len(args) < 2:
                print("Usage: slm info <model-name>")
                sys.exit(1)
            cmd_info(index, " ".join(args[1:]))
        elif cmd == "task":
            if len(args) < 2:
                print("Usage: slm task <task-id>")
                sys.exit(1)
            cmd_task(index, args[1])
        elif cmd == "compare":
            if len(args) < 3:
                print("Usage: slm compare <model1> <model2>")
                sys.exit(1)
            cmd_compare(index, args[1], args[2])
        elif cmd == "hardware":
            target = args[1] if len(args) > 1 else ""
            cmd_hardware(index, target)
        elif cmd == "leaderboard":
            cmd_leaderboard(index)
        elif cmd == "stats":
            cmd_stats(index)
        else:
            print(f"Unknown command: {cmd}")
            print(f"Run 'slm --help' for usage information.")
            sys.exit(1)
    except BrokenPipeError:
        pass


if __name__ == "__main__":
    main()
