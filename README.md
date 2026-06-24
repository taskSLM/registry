# 🚀 Task-Specific SLM Registry

The community-curated registry for highly optimized, **Small Language Models (SLMs)** under 8B parameters and the datasets that power them. 

Built for edge computing, local deployment, privacy, and hyper-specific automation tasks.

---

## 📂 Core Directory

We organize our data using a strict, data-first structure. You can browse the existing files directly in the repository folders:

* **[📁 models/](./models)** — Specialized, compact models (sub-8B) optimized for local or efficient production use.
* **[📁 datasets/](./datasets)** — Clean, target-specific datasets ideal for fine-tuning or evaluation.
* **[📁 tasks/](./tasks)** — Standardized definitions of narrow NLP and code generation tasks.

### Featured Seed Additions:
* **Model:** [Phi-3-mini-4k-instruct](./models/phi-3-mini.yaml) (3.8B parameters)
* **Dataset:** [SQL-Create-Context](./datasets/sql-create-context.yaml) (78k text-to-SQL rows)
* **Task:** [Text-to-SQL Generation](./tasks/text-to-sql.yaml)

---

## 🤝 How to Contribute

This is a completely community-supported initiative. If you have fine-tuned an SLM, quantized a model for edge hardware, or curated a specific dataset, we want it here!

### Submission Rules:
1. **Size Cap:** Models must be strictly **under 8 Billion parameters**.
2. **Task Specificity:** The model or dataset must solve or evaluate a distinct, narrow task.
3. **Open Access:** Links to download weights or data must be publicly available (e.g., Hugging Face).

*(Automated issue forms and submission templates coming soon!)*

---

## 📜 License

This registry's metadata and structure are open-source and licensed under the **MIT License**. All linked models and datasets retain their respective original creator licenses.
