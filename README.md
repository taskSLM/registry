# 🤖 SLM World — The World's Largest Small Language Model Registry

<div align="center">

[![Models](https://img.shields.io/badge/models-11-blue)](models/)
[![Datasets](https://img.shields.io/badge/datasets-6-green)](datasets/)
[![Tasks](https://img.shields.io/badge/tasks-9-orange)](tasks/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen)](CONTRIBUTING.md)

**The community-curated registry of Small Language Models (sub-8B), the tasks they solve, and the datasets that power them.**

[Browse Models](models/) · [Browse Tasks](tasks/) · [Browse Datasets](datasets/) · [Contribute](CONTRIBUTING.md)

</div>

---

## Why SLM World?

Small Language Models are eating the world. They run on your phone, your laptop, your Raspberry Pi. They're private, fast, and cheap. But finding the *right* SLM for a specific task is still a nightmare — scattered across Hugging Face, random blog posts, and Twitter threads.

**SLM World fixes this.** We're building the definitive, human-curated map of:

- **🔍 Which SLM to use** for any specific task (Text-to-SQL, code generation, function calling...)
- **📊 How they compare** — benchmarks, hardware requirements, deployment readiness
- **📚 What data to use** for fine-tuning or evaluation
- **🔗 How everything connects** — models → tasks → datasets, fully cross-referenced

All under **permissive licenses** (Apache 2.0, MIT, CC-BY). No research-only restrictions. No "email us for commercial use." Just open, usable models and data.

---

## 📂 The Registry

### Architecture: Three Interlinked Directories

```text
                    ┌──────────────┐
                    │    TASKS     │  ← The Hub: defines problems,
                    │    (9)       │     links models ↔ datasets
                    └──┬────────┬──┘
           recommends  │        │  recommends
              models   │        │  datasets
                       ▼        ▼
                 ┌────────┐ ┌──────────┐
                 │ MODELS │ │ DATASETS │  ← The Solvers & The Fuel
                 │  (11)  │ │   (6)    │
                 └────────┘ └──────────┘
```

Every task links to its best models and eval datasets. Every model and dataset links back through tasks. No loose string matching — real file references you can follow.

### Quick Stats

| | Count | Highlights |
|---|-------|------------|
| **Models** | 11 | From 135M to 7.6B params, 8 developers, 5 license types |
| **Datasets** | 6 | From 10K to 14M rows, covering math, code, SQL, chat, alignment |
| **Tasks** | 9 | Text-to-SQL, Code Gen, Math, Function Calling, Multimodal, and more |

---

## 🚀 Quick Start

### Find a model for your task

```bash
# Browse by task — every task lists its recommended models
# Open tasks/code-generation.yaml and scroll to recommended_models:
```

Or browse directly:
- **[General Reasoning](tasks/general-reasoning.yaml)** — Qwen3.5-4B, TinyLlama, Phi-4-mini, SmolLM3
- **[Code Generation](tasks/code-generation.yaml)** — Gemma 3 4B, Qwen2.5-7B, SmolLM3
- **[Math Reasoning](tasks/math-reasoning.yaml)** — Gemma 3 4B, Qwen2.5-7B, Qwen3.5-4B
- **[Function Calling](tasks/function-calling.yaml)** — Granite-3.2-2B, Llama 3.2 3B, SmolLM3
- **[Multimodal](tasks/multimodal-reasoning.yaml)** — Gemma 3 4B, Gemma 4 E2B
- **[Text-to-SQL](tasks/text-to-sql.yaml)** — Qwen2.5-7B, Phi-4-mini
- **[Knowledge QA](tasks/knowledge-qa.yaml)** — Phi-4-mini, Qwen3.5-4B, OLMo-7B
- **[Instruction Following](tasks/instruction-following.yaml)** — Qwen3.5-4B, SmolLM3, OLMo-7B
- **[Preference Alignment](tasks/preference-alignment.yaml)** — UltraFeedback DPO

### Find a dataset for fine-tuning

| Task | Best Dataset | Size | License |
|------|-------------|------|---------|
| Math | [OpenMathInstruct-2](datasets/openmathinstruct-2.yaml) | 14M rows | CC-BY-4.0 |
| Code | [Magicoder-Evol-Instruct-110K](datasets/magicoder-evol-instruct-110k.yaml) | 110K rows | MIT |
| Chat/Instruct | [smoltalk](datasets/smoltalk.yaml) | 1.1M rows | Apache 2.0 |
| Text-to-SQL | [SQL-Create-Context](datasets/sql-create-context.yaml) | 78K rows | MIT |
| Text-to-SQL Eval | [Spider](datasets/spider.yaml) | 10K rows | CC-BY-SA-4.0 |
| DPO Alignment | [UltraFeedback](datasets/ultrafeedback-binarized-preferences.yaml) | 61K rows | MIT |

---

## 📊 Featured Models

| Model | Params | Context | License | Best For |
|-------|--------|---------|---------|----------|
| [Qwen3.5-4B](models/qwen3-5-4b.yaml) | 4.0B | 256K | Apache 2.0 | Best all-around SLM |
| [Gemma 3 4B](models/gemma-3-4b-it.yaml) | 4.0B | 128K | Apache 2.0 | Code + multimodal |
| [SmolLM3-3B](models/smollm3-3b.yaml) | 3.0B | 64K | Apache 2.0 | Fully open (data+code+weights) |
| [Phi-4-mini](models/phi-4-mini-instruct.yaml) | 3.8B | 4K | MIT | Best reasoning at size |
| [Qwen2.5-7B](models/qwen2-5-7b-instruct.yaml) | 7.6B | 128K | Apache 2.0 | Top of sub-8B range |
| [TinyLlama-1.1B](models/tinyllama-1-1b.yaml) | 1.1B | 2K | Apache 2.0 | Best 1B baseline |
| [Granite-3.2-2B](models/granite-3-2-2b-instruct.yaml) | 2.0B | 128K | Apache 2.0 | Enterprise function calling |
| [Gemma 4 E2B](models/gemma-4-e2b-it.yaml) | 2.3B | 128K | Apache 2.0 | Multimodal edge AI |
| [Llama 3.2 3B](models/llama-3-2-3b-instruct.yaml) | 3.0B | 128K | Llama Community | Tool calling |
| [OLMo-7B](models/olmo-7b-instruct.yaml) | 7.0B | 2K | Apache 2.0 | Open science |
| [Phi-3-mini](models/phi-3-mini.yaml) | 3.8B | 4K | MIT | Lightweight baseline |

---

## 🤝 Contributing

We want **your** models, datasets, and tasks. Whether you've fine-tuned an SLM, curated a dataset, or benchmarked models for a specific task — this registry needs it.

### Three ways to contribute:

| You have... | Do this | Takes |
|-------------|---------|-------|
| A model to add | [Open a Model Submission](https://github.com/taskSLM/registry/issues/new?template=submit-model.yml) | 2 minutes |
| A dataset to add | [Open a Dataset Submission](https://github.com/taskSLM/registry/issues/new?template=submit-dataset.yml) | 2 minutes |
| A new task definition | [Open a Task Submission](https://github.com/taskSLM/registry/issues/new?template=submit-task.yml) | 5 minutes |

An auto-PR pipeline handles the rest — your submission becomes a YAML file and a pull request is opened automatically. A maintainer reviews and merges within 48 hours.

**Eligibility rules:**
1. **Models:** Strictly under 8B parameters, weights publicly accessible, permissive license
2. **Datasets:** Permissive license (MIT, Apache 2.0, CC-BY, CC-BY-SA), publicly accessible
3. **Tasks:** Narrow, well-defined NLP/code task with measurable metrics

Full details in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 🔧 Programmatic Access

The registry exposes an auto-generated `index.json` for programmatic consumption:

```bash
# Fetch the latest index
curl -L https://raw.githubusercontent.com/taskSLM/registry/main/index.json

# Or use the CLI
pip install slm-registry
slm search "code generation"
slm info phi-4-mini
slm list --task text-to-sql
```

---

## 📜 License

The registry metadata (YAML files, index, tooling) is licensed under **MIT**. Each linked model and dataset retains its original license — clearly documented in every YAML file's `license` field.

---

## ⭐ Acknowledgements

This registry exists because of its contributors. Every merged PR adds to the world's knowledge of small language models. Special thanks to the teams at Microsoft, Google, Alibaba, Meta, Hugging Face, AI2, IBM, EleutherAI, NVIDIA, and the countless open-source developers who build and release these models and datasets under permissive licenses.

---

<div align="center">

**Built by the community, for the community.**  
[Contribute today →](CONTRIBUTING.md)

</div>
