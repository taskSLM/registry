# Tag Taxonomy

Standardized tags for the SLM World Registry. Use these when tagging models, datasets, and tasks.

## Core Capability Tags

| Tag | Description | Use For |
|-----|-------------|---------|
| `reasoning` | Logical deduction, common-sense reasoning, multi-step thinking | General-purpose models |
| `code-generation` | Generating, completing, or translating source code | Code models, coding tasks |
| `math-reasoning` | Mathematical problem solving, proofs, numerical reasoning | Math models, math datasets |
| `multilingual` | Support for multiple (10+) languages | Multilingual models |
| `multimodal` | Processing multiple input types (text + image/audio/video) | Vision-language models |
| `vision` | Image understanding, visual reasoning | Vision-capable models |
| `audio` | Audio/speech processing | Audio-capable models |
| `video` | Video understanding | Video-capable models |
| `tool-calling` | Invoking external tools, APIs, or functions | Agentic models |
| `function-calling` | Structured function/API invocation (synonym: tool-calling) | Enterprise models |
| `agentic` | Autonomous multi-step task execution with tools | Agent frameworks |
| `chat` | Conversational ability, multi-turn dialogue | Chat models |
| `instruction-following` | Accurately executing natural language instructions | Instruct-tuned models |
| `knowledge-qa` | Factual question answering from encoded knowledge | QA models |
| `text-to-sql` | Translating natural language to SQL queries | Database models |
| `summarization` | Condensing long text into shorter summaries | Summarization models |
| `translation` | Translating between languages | Translation models |
| `named-entity-recognition` | Identifying entities (names, places, dates) in text | NER models |
| `sentiment-analysis` | Classifying text sentiment/emotion | Classification models |

## Deployment & Hardware Tags

| Tag | Description | Use For |
|-----|-------------|---------|
| `edge-computing` | Suitable for edge/serverless deployment | Small footprint models |
| `on-device` | Runs directly on phones, IoT, embedded devices | Tiny models |
| `mobile` | Optimized for mobile deployment (iOS/Android) | Mobile-optimized models |
| `lightweight` | Low memory/disk footprint, fast inference | Resource-constrained use |
| `efficient` | Strong performance relative to parameter count | Pareto-optimal models |
| `production` | Battle-tested, stable, monitored in prod | Enterprise-ready models |
| `local-llm` | Designed for fully local/offline use | Privacy-focused deployment |

## Quality & Openness Tags

| Tag | Description | Use For |
|-----|-------------|---------|
| `open-source` | Weights publicly available under permissive license | Most registry models |
| `fully-open` | Weights + training data + code all public | Transparent models |
| `reproducible` | Training process fully documented and reproducible | Research models |
| `research` | Primarily intended for academic/research use | Research-focused entries |
| `community` | Strong community ecosystem, many forks/variants | Popular models |
| `benchmark` | Standard evaluation benchmark | Eval datasets |
| `baseline` | Good reference point for comparison | Baseline models |

## Data-Specific Tags

| Tag | Description | Use For |
|-----|-------------|---------|
| `fine-tuning` | Dataset suitable for supervised fine-tuning (SFT) | Training datasets |
| `evaluation` | Dataset designed for model evaluation/benchmarking | Eval datasets |
| `synthetic-data` | Artificially generated (not human-created) | Synthetic datasets |
| `large-scale` | >1M rows/examples | Large datasets |
| `chain-of-thought` | Includes step-by-step reasoning traces | Reasoning datasets |
| `decontaminated` | Cleaned of benchmark/test-set contamination | Clean datasets |
| `multi-table` | Involves multiple database tables | SQL datasets |
| `complex-sql` | Contains nested queries, JOINs, subqueries | Advanced SQL data |
| `multi-language` | Contains multiple programming languages | Code datasets |
| `structured-output` | Requires formatted output (JSON, XML, YAML) | Structured generation |
| `structured-data` | Involves structured/tabular data | Database-related entries |

## Alignment & Safety Tags

| Tag | Description | Use For |
|-----|-------------|---------|
| `alignment` | Model aligned with human preferences | Aligned models |
| `dpo` | Trained with Direct Preference Optimization | DPO-trained models |
| `rlhf` | Trained with RL from Human Feedback | RLHF-trained models |
| `safety` | Evaluated for safety, harmlessness, refusal | Safety-focused entries |
| `post-training` | Used in post-training / alignment stage | Alignment datasets |
| `preference-tuning` | Contains preference pairs (chosen vs rejected) | DPO datasets |

## Utility Tags

| Tag | Description | Use For |
|-----|-------------|---------|
| `long-context` | Supports 32K+ token context windows | Long-document models |
| `thinking-mode` | Has explicit reasoning/thinking toggle | Reasoning models |
| `high-performance` | Top-tier performance in its size class | Best-in-class models |

---

## Usage Guidelines

1. **Prefer standard tags.** Check this list before inventing a new tag — there's probably one that fits.
2. **Use 2-6 tags per entry.** Enough to be discoverable, not so many that every entry matches.
3. **Capability tags first.** Lead with what the model/dataset *does*, then deployment characteristics.
4. **Propose new tags.** If you genuinely need a new tag, open an issue to add it to this taxonomy. The validation CI will warn on unknown tags but won't block your submission.
5. **Tags are lowercase, hyphenated.** Follow the existing convention: `code-generation` not `Code Generation` or `code_generation`.
