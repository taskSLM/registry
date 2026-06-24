# Contributing to the SLM World Registry 🚀

Thank you for helping build the world's largest registry of Small Language Models! This guide covers everything you need to contribute.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Quick Start: Submit a Model](#quick-start-submit-a-model)
- [YAML Field Reference](#yaml-field-reference)
  - [Model Schema](#model-schema)
  - [Dataset Schema](#dataset-schema)
  - [Task Schema](#task-schema)
- [How the Auto-PR Pipeline Works](#how-the-auto-pr-pipeline-works)
- [License Requirements](#license-requirements)
- [Review Process](#review-process)
- [Becoming a Maintainer](#becoming-a-maintainer)
- [Development Setup](#development-setup)
- [Tag Taxonomy](#tag-taxonomy)

---

## Code of Conduct

This project is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). All contributors are expected to uphold it. TL;DR: be respectful, constructive, and inclusive.

## Ways to Contribute

| What | How | Difficulty |
|------|-----|------------|
| **Add a model** | [Open an issue](https://github.com/taskSLM/registry/issues/new?template=submit-model.yml) using the Model Submission form | ⭐ Easy |
| **Add a dataset** | [Open an issue](https://github.com/taskSLM/registry/issues/new?template=submit-dataset.yml) using the Dataset Submission form | ⭐ Easy |
| **Add a task** | [Open an issue](https://github.com/taskSLM/registry/issues/new?template=submit-task.yml) using the Task Submission form | ⭐⭐ Medium |
| **Improve existing entries** | Edit the YAML file directly and open a PR | ⭐⭐ Medium |
| **Fix bugs / add features** | See [Development Setup](#development-setup) | ⭐⭐⭐ Advanced |
| **Review community PRs** | Comment on open PRs with feedback | ⭐⭐ Medium |
| **Spread the word** | Star the repo, share on social media, write blog posts | ⭐ Easy |

## Quick Start: Submit a Model

1. **Check it's not already listed** — browse the [`models/`](models/) directory.
2. **Verify eligibility:**
   - Model is **strictly under 8 billion parameters**
   - Weights are **publicly accessible** (e.g., Hugging Face)
   - License is **permissive** (Apache 2.0, MIT, CC-BY, BSD, or equivalent)
3. **Open a Model Submission issue** — fill out the form with the model's details.
4. **A PR is auto-generated** — our bot creates a YAML file and opens a pull request.
5. **A maintainer reviews and merges** — usually within 48 hours.

Same flow applies for datasets and tasks using their respective issue forms.

---

## YAML Field Reference

### Model Schema

```yaml
# Required fields
name: "Qwen3.5-4B"                    # Exact model name as on Hugging Face
developer: "Alibaba"                   # Organization or team that created the model
parameters: "4.0B"                     # Human-readable parameter count (e.g., "3.8B", "760M")
primary_task: "General Reasoning"      # The main task this model excels at
context_window: "256K tokens"          # Maximum context length
license: "Apache 2.0"                  # License of the model weights
huggingface_url: "https://huggingface.co/Qwen/Qwen3.5-4B"  # Direct URL to model
description: >                         # 2-4 sentences describing the model's strengths,
  A state-of-the-art 4B model...       #   use cases, and notable benchmarks

# Optional but recommended fields
tags:                                  # See Tag Taxonomy section below
  - reasoning
  - multilingual
  - instruction-following
predecessor: "models/qwen3-4b.yaml"   # Previous model in the same family (if any)
param_count_m: 4000                    # Exact parameter count in millions (for programmatic use)
```

**Field rules:**
- `name`: Use the exact name from Hugging Face. Include the variant suffix (e.g., `-Instruct`, `-it`).
- `parameters`: Use B for billions, M for millions. Include notes about MoE architecture if applicable.
- `license`: Use the standard SPDX identifier or well-known name. Common values: `Apache 2.0`, `MIT`, `CC-BY-4.0`, `Llama Community License`.
- `huggingface_url`: Must be a direct link to the model page, not a collection or search URL.
- `tags`: Use tags from the [standardized taxonomy](TAGS.md). Custom tags are allowed but may be normalized by maintainers.

### Dataset Schema

```yaml
# Required fields
name: "OpenMathInstruct-2"             # Exact dataset name as on Hugging Face
creator: "NVIDIA"                      # Organization or team that created the dataset
size_rows: "14,000,000"                # Number of rows/examples
target_task: "Math Reasoning"          # The task this dataset is designed for
license: "CC-BY-4.0"                   # License of the dataset
huggingface_url: "https://huggingface.co/datasets/nvidia/OpenMathInstruct-2"
description: >                         # 2-4 sentences describing the dataset's content,
  A massive 14M-row math dataset...    #   structure, and intended use

# Optional but recommended fields
tags:
  - math-reasoning
  - chain-of-thought
  - fine-tuning
  - synthetic-data
```

### Task Schema

```yaml
# Required fields
task_id: "code-generation"             # URL-safe unique ID (lowercase, hyphens)
display_name: "Code Generation"        # Human-readable name
domain: "Software Engineering"         # High-level category
description: >                         # What this task involves and tests
  The process of generating...
input_format: "Natural language..."    # What the model receives
output_format: "Source code..."        # What the model should produce
metrics_tracked:                       # Standard evaluation metrics
  - Pass@1
  - HumanEval Score

# Recommended fields
recommended_models:                    # Models known to perform well on this task
  - ref: "models/gemma-3-4b-it.yaml"
    notes: "71.3% HumanEval — top code performer at 4B scale."
recommended_datasets:                  # Datasets for training/evaluating this task
  - ref: "datasets/magicoder-evol-instruct-110k.yaml"
    purpose: "fine-tuning"
related_tasks:                         # Links to parent/child/related tasks
  - task_id: "instruction-following"
    relationship: "parent"
```

**`related_tasks` relationship values:**
- `parent` — broader task that encompasses this one
- `child` — narrower specialization of this task
- `related` — similar but distinct task
- `enhances` — meta-task that improves performance on this task (e.g., preference alignment)

---

## How the Auto-PR Pipeline Works

```text
You open an issue        GitHub Actions fires       A PR is auto-created       Maintainer reviews
using the form    →      parses the form data  →    with the YAML file    →   & merges to main
                         writes models/*.yaml        on branch submit/*
```

The workflow (`submit-model.yml`) does this:
1. Parses your issue form responses using `github-issue-forms-parser`
2. Generates a properly formatted YAML file in the correct directory
3. Creates a new branch (`submit/<model-name>`)
4. Opens a pull request targeting `main`
5. Comments on your issue with a link to the PR

**If the auto-PR fails:** A maintainer will manually create the YAML from your issue. Your contribution still counts!

---

## License Requirements

### For Models
The model weights must be under a **permissive open-source license**. Accepted licenses:
- ✅ Apache 2.0
- ✅ MIT
- ✅ BSD (2-clause, 3-clause)
- ✅ CC-BY-4.0
- ✅ Llama Community License (permissive with acceptable use policy)
- ❌ Non-commercial only (CC-BY-NC, etc.) — does not qualify
- ❌ Research-only / custom restrictive licenses — does not qualify
- ❌ No license specified — does not qualify

### For Datasets
Datasets should also be permissively licensed. Accepted licenses include all model licenses plus:
- ✅ CC-BY-SA-4.0 (ShareAlike is acceptable for data)
- ✅ CC0 (public domain)
- ✅ ODC-BY

### Scope
The registry metadata itself is MIT-licensed. The models and datasets you link to retain their original licenses — we just index them.

---

## Review Process

1. **Automated checks run first** — YAML validity, URL reachability, field completeness
2. **A maintainer reviews** for:
   - Accuracy of information (parameter count, license, task fit)
   - No duplicate entries
   - Description quality (not copy-pasted marketing, actually useful)
   - Tags are appropriate
3. **Feedback is posted on the PR** if changes are needed
4. **Once approved**, the PR is merged and your contribution is live!

**Typical turnaround:** 24–48 hours. If it's been longer, feel free to ping the PR with a comment.

---

## Becoming a Maintainer

We actively grow the maintainer team from our most consistent contributors.

**Path to maintainer:**
1. Get **5+ contributions merged** (models, datasets, tasks, or code)
2. Provide **helpful reviews** on 3+ community PRs
3. Demonstrate understanding of the [YAML schema](#yaml-field-reference) and [license rules](#license-requirements)
4. Open an issue titled "Maintainer Nomination: @your-username" explaining your interest

**Maintainer responsibilities:**
- Review and merge community PRs
- Keep the registry consistent and high-quality
- Help improve automation and tooling
- Uphold the Code of Conduct

Maintainers who are inactive for 6+ months are moved to emeritus status (always welcome back!).

---

## Development Setup

Want to improve the registry tooling itself? Here's how to get started.

### Prerequisites
- Python 3.10+
- `pip install pyyaml requests`

### Running validation locally
```bash
# Validate all YAML files
python scripts/validate.py

# Validate a specific file
python scripts/validate.py models/phi-4-mini-instruct.yaml

# Check cross-references
python scripts/validate.py --check-refs
```

### Running the index generator locally
```bash
# Generate index.json from all YAML files
python scripts/generate_index.py

# Output to specific path
python scripts/generate_index.py --output dist/index.json
```

### Project structure
```text
slm-world/
├── models/              # Model YAML definitions
├── datasets/            # Dataset YAML definitions
├── tasks/               # Task YAML definitions (the connecting hub)
├── scripts/             # Validation and generation scripts
├── .github/
│   ├── ISSUE_TEMPLATE/  # Issue forms for submissions
│   └── workflows/       # CI/CD automation
├── index.json           # Auto-generated registry index
├── TAGS.md              # Standardized tag taxonomy
└── CONTRIBUTING.md      # You are here
```

---

## Tag Taxonomy

We maintain a [standardized tag vocabulary](TAGS.md) to keep the registry searchable and consistent. Before adding custom tags, check if a standard tag already fits.

Common tags by category:
- **Capability:** `reasoning`, `code-generation`, `math-reasoning`, `multilingual`, `multimodal`, `vision`, `audio`
- **Deployment:** `edge-computing`, `on-device`, `mobile`, `lightweight`, `efficient`
- **Use case:** `tool-calling`, `function-calling`, `agentic`, `chat`, `instruction-following`, `knowledge-qa`
- **Quality:** `open-source`, `fully-open`, `reproducible`, `research`

See [TAGS.md](TAGS.md) for the complete controlled vocabulary.

---

*This registry thrives because of contributors like you. Every model, dataset, and task you add helps someone find the right tool for their job. Thank you!* 🚀
