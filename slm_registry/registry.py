"""
Registry data loader — fetches and caches the SLM World index.json.

Supports loading from:
  - A local index.json file
  - The GitHub raw URL (auto-caches to disk)
  - A custom URL
"""

import json
import os
import time
from pathlib import Path
from typing import Optional

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request


DEFAULT_INDEX_URL = (
    "https://raw.githubusercontent.com/taskSLM/registry/main/index.json"
)
CACHE_DIR = Path.home() / ".cache" / "slm-registry"
CACHE_TTL = 3600  # 1 hour in seconds


def _load_local(path: Path) -> dict:
    """Load index from a local file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_remote(url: str, cache_path: Path) -> dict:
    """Fetch index from URL and cache it."""
    req = Request(url, headers={"User-Agent": "slm-registry-cli/1.0"})
    with urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return data


def load_index(
    local_path: Optional[str] = None,
    remote_url: Optional[str] = None,
    force_refresh: bool = False,
) -> dict:
    """
    Load the registry index.

    Priority:
    1. Explicit local_path
    2. Explicit remote_url
    3. Default GitHub URL (with local cache)
    4. Look for index.json in cwd and parent directories
    """
    # 1. Explicit local path
    if local_path:
        p = Path(local_path)
        if p.exists():
            return _load_local(p)
        raise FileNotFoundError(f"Index not found at: {local_path}")

    # 2. Explicit remote URL
    if remote_url:
        cache_path = CACHE_DIR / "index.json"
        if not force_refresh and cache_path.exists():
            age = time.time() - cache_path.stat().st_mtime
            if age < CACHE_TTL:
                return _load_local(cache_path)
        return _load_remote(remote_url, cache_path)

    # 3. Look for local index.json
    for search in [Path.cwd(), Path.cwd().parent]:
        candidate = search / "index.json"
        if candidate.exists():
            return _load_local(candidate)

    # 4. Fall back to GitHub
    cache_path = CACHE_DIR / "index.json"
    if not force_refresh and cache_path.exists():
        age = time.time() - cache_path.stat().st_mtime
        if age < CACHE_TTL:
            return _load_local(cache_path)
    return _load_remote(DEFAULT_INDEX_URL, cache_path)


def get_models(index: dict) -> dict:
    """Get all models from the index."""
    return index.get("models", {})


def get_datasets(index: dict) -> dict:
    """Get all datasets from the index."""
    return index.get("datasets", {})


def get_tasks(index: dict) -> dict:
    """Get all tasks from the index."""
    return index.get("tasks", {})


def search_models(index: dict, query: str) -> list[tuple[str, dict]]:
    """Search models by name, developer, task, tags, or description."""
    query_lower = query.lower()
    results = []
    for key, model in index.get("models", {}).items():
        score = 0
        if query_lower in model.get("name", "").lower():
            score += 10
        if query_lower in model.get("developer", "").lower():
            score += 5
        if query_lower in model.get("primary_task", "").lower():
            score += 8
        if query_lower in model.get("description", "").lower():
            score += 2
        for tag in model.get("tags", []):
            if query_lower in tag.lower():
                score += 6
        for task in model.get("_connected_tasks", []):
            if query_lower in task.lower():
                score += 6
        if score > 0:
            results.append((key, model, score))
    results.sort(key=lambda x: x[2], reverse=True)
    return [(k, m) for k, m, _ in results]


def search_datasets(index: dict, query: str) -> list[tuple[str, dict]]:
    """Search datasets by name, creator, task, or tags."""
    query_lower = query.lower()
    results = []
    for key, ds in index.get("datasets", {}).items():
        score = 0
        if query_lower in ds.get("name", "").lower():
            score += 10
        if query_lower in ds.get("creator", "").lower():
            score += 5
        if query_lower in ds.get("target_task", "").lower():
            score += 8
        if query_lower in ds.get("description", "").lower():
            score += 2
        for tag in ds.get("tags", []):
            if query_lower in tag.lower():
                score += 6
        if score > 0:
            results.append((key, ds, score))
    results.sort(key=lambda x: x[2], reverse=True)
    return [(k, m) for k, m, _ in results]


def get_model_by_name(index: dict, name: str) -> Optional[dict]:
    """Find a model by name (case-insensitive, partial match)."""
    name_lower = name.lower()
    models = index.get("models", {})
    # Exact key match first
    if name_lower in models:
        return models[name_lower]
    # Partial match on name field
    for key, model in models.items():
        if name_lower in model.get("name", "").lower():
            return model
        if name_lower in key.lower():
            return model
    return None


def get_task_by_id(index: dict, task_id: str) -> Optional[dict]:
    """Find a task by ID (case-insensitive)."""
    tasks = index.get("tasks", {})
    task_id_lower = task_id.lower()
    if task_id_lower in tasks:
        return tasks[task_id_lower]
    for key, task in tasks.items():
        if task_id_lower in key.lower():
            return task
        if task_id_lower in task.get("task_id", "").lower():
            return task
    return None


def filter_models_by_hardware(index: dict, target: str) -> list[tuple[str, dict]]:
    """Filter models by hardware compatibility."""
    results = []
    for key, model in index.get("models", {}).items():
        hw = model.get("hardware_compat", {})
        if hw.get(target, False):
            results.append((key, model))
    return results


def get_stats(index: dict) -> dict:
    """Get registry statistics."""
    meta = index.get("meta", {})
    counts = meta.get("counts", {})
    summaries = index.get("summaries", {})

    models = index.get("models", {})
    devices = {
        "raspberry_pi_5": sum(
            1 for m in models.values()
            if m.get("hardware_compat", {}).get("raspberry_pi_5", False)
        ),
        "mobile_phone": sum(
            1 for m in models.values()
            if m.get("hardware_compat", {}).get("mobile_phone", False)
        ),
        "consumer_gpu_8gb": sum(
            1 for m in models.values()
            if m.get("hardware_compat", {}).get("consumer_gpu_8gb", False)
        ),
        "cpu_only": sum(
            1 for m in models.values()
            if m.get("hardware_compat", {}).get("cpu_only", False)
        ),
    }

    return {
        "models": counts.get("models", 0),
        "datasets": counts.get("datasets", 0),
        "tasks": counts.get("tasks", 0),
        "licenses": summaries.get("licenses", {}),
        "param_buckets": summaries.get("param_size_buckets", {}),
        "hardware_compat": devices,
    }
