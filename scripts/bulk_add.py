#!/usr/bin/env python3
"""Bulk YAML generator for models, datasets, and tasks."""
import yaml, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MODELS = [
    # (filename, data_dict)
    ("qwen2.5-0.5b-instruct", {
        "name": "Qwen2.5-0.5B-Instruct", "developer": "Alibaba", "parameters": "0.5B",
        "param_count_m": 500, "primary_task": "Lightweight Instruction Following",
        "context_window": "32K tokens", "license": "Apache 2.0",
        "family": "qwen", "generation": 2.5, "predecessor": None, "successor": None,
        "huggingface_url": "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct",
        "description": "The smallest member of the Qwen2.5 family at 0.5B parameters. Surprisingly capable for its size, supporting 29+ languages and 32K context. Ideal for resource-constrained environments, on-device deployment, and as a minimal baseline for fine-tuning experiments.",
        "badges": ["verified"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 0.3, "recommended_backend": "llama.cpp"},
        "tags": ["lightweight", "multilingual", "on-device", "efficient", "instruction-following", "tiny"]
    }),
    ("qwen2.5-1.5b-instruct", {
        "name": "Qwen2.5-1.5B-Instruct", "developer": "Alibaba", "parameters": "1.5B",
        "param_count_m": 1500, "primary_task": "General Reasoning & Instruction Following",
        "context_window": "32K tokens", "license": "Apache 2.0",
        "family": "qwen", "generation": 2.5, "predecessor": None, "successor": None,
        "huggingface_url": "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct",
        "description": "A compact 1.5B model from Alibaba's Qwen2.5 series. Balances strong performance with minimal resource requirements. Supports 29+ languages and delivers solid reasoning, chat, and instruction-following at a fraction of the cost of larger models.",
        "badges": ["verified"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 0.9, "recommended_backend": "llama.cpp"},
        "tags": ["lightweight", "multilingual", "reasoning", "instruction-following", "efficient"]
    }),
    ("qwen2.5-3b-instruct", {
        "name": "Qwen2.5-3B-Instruct", "developer": "Alibaba", "parameters": "3.1B",
        "param_count_m": 3100, "primary_task": "General Reasoning & Code Generation",
        "context_window": "32K tokens", "license": "Apache 2.0",
        "family": "qwen", "generation": 2.5, "predecessor": None, "successor": None,
        "huggingface_url": "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct",
        "description": "The 3B variant of Qwen2.5 offering strong reasoning and code generation at a highly efficient size. Hits the sweet spot between TinyLlama-1.1B and 7B models for quality-per-parameter. Supports 29+ languages with solid instruction following.",
        "badges": ["verified"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 1.9, "recommended_backend": "llama.cpp"},
        "tags": ["reasoning", "code-generation", "multilingual", "instruction-following", "efficient"]
    }),
    ("smollm2-135m-instruct", {
        "name": "SmolLM2-135M-Instruct", "developer": "Hugging Face", "parameters": "135M",
        "param_count_m": 135, "primary_task": "Lightweight Instruction Following",
        "context_window": "8K tokens", "license": "Apache 2.0",
        "family": "smollm", "generation": 2, "predecessor": None, "successor": "models/smollm3-3b.yaml",
        "huggingface_url": "https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct",
        "description": "The smallest model in the SmolLM2 family at just 135M parameters. Remarkably capable for its size with basic instruction following and chat abilities. Fully open (weights + data + code). Ideal for embedded systems, research on tiny models, and extreme edge deployment.",
        "badges": ["verified", "fully-open"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 0.1, "recommended_backend": "llama.cpp"},
        "tags": ["lightweight", "tiny", "on-device", "fully-open", "efficient"]
    }),
    ("smollm2-360m-instruct", {
        "name": "SmolLM2-360M-Instruct", "developer": "Hugging Face", "parameters": "360M",
        "param_count_m": 360, "primary_task": "Lightweight Instruction Following",
        "context_window": "8K tokens", "license": "Apache 2.0",
        "family": "smollm", "generation": 2, "predecessor": None, "successor": "models/smollm3-3b.yaml",
        "huggingface_url": "https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct",
        "description": "A 360M parameter instruction-tuned model from the SmolLM2 family. Provides a step up from the 135M variant with noticeably better reasoning and instruction following. Fully open (weights + data + code). Great for resource-constrained environments and research on small model capabilities.",
        "badges": ["verified", "fully-open"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 0.2, "recommended_backend": "llama.cpp"},
        "tags": ["lightweight", "tiny", "on-device", "fully-open", "efficient"]
    }),
    ("smollm2-1.7b-instruct", {
        "name": "SmolLM2-1.7B-Instruct", "developer": "Hugging Face", "parameters": "1.7B",
        "param_count_m": 1700, "primary_task": "General Reasoning & Instruction Following",
        "context_window": "8K tokens", "license": "Apache 2.0",
        "family": "smollm", "generation": 2, "predecessor": None, "successor": "models/smollm3-3b.yaml",
        "huggingface_url": "https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct",
        "description": "The largest SmolLM2 model at 1.7B parameters. Trained on the fully open smoltalk dataset and delivers strong reasoning and chat abilities. Complete transparency — weights, training data, and code are all publicly available. Excellent for research, fine-tuning, and deployment on consumer hardware.",
        "badges": ["verified", "fully-open"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 1.0, "recommended_backend": "llama.cpp"},
        "tags": ["reasoning", "fully-open", "instruction-following", "efficient", "chat"]
    }),
    ("gemma-2-2b-it", {
        "name": "Gemma 2 2B IT", "developer": "Google DeepMind", "parameters": "2.6B",
        "param_count_m": 2600, "primary_task": "General Reasoning & Chat",
        "context_window": "8K tokens", "license": "Apache 2.0",
        "family": "gemma", "generation": 2, "predecessor": None, "successor": "models/gemma-3-4b-it.yaml",
        "huggingface_url": "https://huggingface.co/google/gemma-2-2b-it",
        "description": "Google's Gemma 2 at 2.6B parameters. Punching well above its weight class, this model delivers competitive performance against much larger models. Known for strong reasoning, clean outputs, and efficient deployment. Predecessor to the Gemma 3 4B, showing Google's progression in the small model space.",
        "badges": ["verified"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 1.6, "recommended_backend": "llama.cpp"},
        "tags": ["reasoning", "chat", "efficient", "instruction-following"]
    }),
    ("gemma-3-1b-it", {
        "name": "Gemma 3 1B IT", "developer": "Google DeepMind", "parameters": "1.0B",
        "param_count_m": 1000, "primary_task": "Lightweight Multimodal Reasoning",
        "context_window": "32K tokens", "license": "Apache 2.0",
        "family": "gemma", "generation": 3, "predecessor": None, "successor": None,
        "huggingface_url": "https://huggingface.co/google/gemma-3-1b-it",
        "description": "The smallest Gemma 3 variant at 1B parameters, supporting both text and image inputs. A remarkably capable tiny multimodal model that fits on virtually any device. Perfect for mobile vision-language tasks, on-device image understanding, and lightweight multimodal assistants.",
        "badges": ["verified"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 0.6, "recommended_backend": "llama.cpp"},
        "tags": ["multimodal", "vision", "tiny", "mobile", "on-device", "lightweight"]
    }),
    ("phi-3.5-mini-instruct", {
        "name": "Phi-3.5-mini-instruct", "developer": "Microsoft", "parameters": "3.8B",
        "param_count_m": 3800, "primary_task": "General Reasoning & Multilingual",
        "context_window": "128K tokens", "license": "MIT",
        "family": "phi", "generation": 3.5, "predecessor": "models/phi-3-mini.yaml", "successor": "models/phi-4-mini-instruct.yaml",
        "huggingface_url": "https://huggingface.co/microsoft/Phi-3.5-mini-instruct",
        "description": "The bridge between Phi-3 and Phi-4 at 3.8B parameters. Added 128K context window and significantly improved multilingual capabilities over Phi-3-mini. Retains the strong reasoning of the Phi family while enabling long-document processing and cross-lingual tasks. MIT licensed for maximum flexibility.",
        "badges": ["verified"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 2.4, "recommended_backend": "llama.cpp"},
        "tags": ["reasoning", "multilingual", "long-context", "lightweight", "local-llm"]
    }),
    ("phi-3-mini-128k-instruct", {
        "name": "Phi-3-mini-128k-instruct", "developer": "Microsoft", "parameters": "3.8B",
        "param_count_m": 3800, "primary_task": "Long-Context Reasoning",
        "context_window": "128K tokens", "license": "MIT",
        "family": "phi", "generation": 3, "predecessor": None, "successor": "models/phi-3.5-mini-instruct.yaml",
        "huggingface_url": "https://huggingface.co/microsoft/Phi-3-mini-128k-instruct",
        "description": "Long-context variant of Phi-3-mini with 128K token context window. Same strong reasoning capabilities as the 4K version but capable of processing entire books, lengthy documents, and extended conversations. MIT licensed. A strong choice for RAG alternatives and long-document QA.",
        "badges": ["verified"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 2.2, "recommended_backend": "llama.cpp"},
        "tags": ["long-context", "reasoning", "lightweight", "local-llm"]
    }),
    ("llama-3.2-1b-instruct", {
        "name": "Llama 3.2 1B Instruct", "developer": "Meta", "parameters": "1.0B",
        "param_count_m": 1000, "primary_task": "Lightweight Instruction Following",
        "context_window": "128K tokens", "license": "Llama 3.2 Community License",
        "family": "llama", "generation": 3.2, "predecessor": None, "successor": None,
        "huggingface_url": "https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct",
        "description": "Meta's smallest Llama 3.2 model at 1B parameters with 128K context. Optimized for mobile and on-device deployment with surprisingly strong instruction following and structured output. Pairs with Llama 3.2 3B as Meta's push into truly portable AI.",
        "badges": ["verified"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 0.6, "recommended_backend": "llama.cpp"},
        "tags": ["lightweight", "mobile", "on-device", "tool-calling", "instruction-following"]
    }),
    ("pythia-1.4b", {
        "name": "Pythia-1.4B", "developer": "EleutherAI", "parameters": "1.4B",
        "param_count_m": 1400, "primary_task": "Research & Reproducibility",
        "context_window": "2K tokens", "license": "Apache 2.0",
        "family": "pythia", "generation": 1, "predecessor": None, "successor": None,
        "huggingface_url": "https://huggingface.co/EleutherAI/pythia-1.4b",
        "description": "Part of EleutherAI's Pythia scaling suite — a set of 8 model sizes all trained on the same data in the same order. The 1.4B variant provides an excellent mid-size baseline for controlled experiments on model scaling, training dynamics, and interpretability. Apache 2.0 licensed with full training data available.",
        "badges": ["verified", "baseline"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 0.9, "recommended_backend": "llama.cpp"},
        "tags": ["research", "reproducible", "baseline", "open-source"]
    }),
    ("pythia-2.8b", {
        "name": "Pythia-2.8B", "developer": "EleutherAI", "parameters": "2.8B",
        "param_count_m": 2800, "primary_task": "Research & Reproducibility",
        "context_window": "2K tokens", "license": "Apache 2.0",
        "family": "pythia", "generation": 1, "predecessor": None, "successor": None,
        "huggingface_url": "https://huggingface.co/EleutherAI/pythia-2.8b",
        "description": "The 2.8B member of EleutherAI's Pythia scaling suite. Trained on the exact same data as all other Pythia models, enabling controlled experiments on how model capabilities emerge with scale. All 154 training checkpoints are available for studying training dynamics. Apache 2.0.",
        "badges": ["verified", "baseline"], "hardware_compat": {"raspberry_pi_5": True, "mobile_phone": True, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 1.7, "recommended_backend": "llama.cpp"},
        "tags": ["research", "reproducible", "baseline", "open-source"]
    }),
    ("pythia-6.9b", {
        "name": "Pythia-6.9B", "developer": "EleutherAI", "parameters": "6.9B",
        "param_count_m": 6900, "primary_task": "Research & Reproducibility",
        "context_window": "2K tokens", "license": "Apache 2.0",
        "family": "pythia", "generation": 1, "predecessor": None, "successor": None,
        "huggingface_url": "https://huggingface.co/EleutherAI/pythia-6.9b",
        "description": "The largest model in EleutherAI's Pythia scaling suite at 6.9B parameters. Part of a controlled experiment across 8 model sizes (70M to 12B) all trained identically on The Pile. With 154 released checkpoints per model, Pythia is the gold standard for studying how language model capabilities develop during training.",
        "badges": ["verified", "baseline"], "hardware_compat": {"raspberry_pi_5": False, "mobile_phone": False, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 4.1, "recommended_backend": "llama.cpp"},
        "tags": ["research", "reproducible", "baseline", "open-source", "high-performance"]
    }),
    ("falcon-7b-instruct", {
        "name": "Falcon-7B-Instruct", "developer": "Technology Innovation Institute", "parameters": "7.0B",
        "param_count_m": 7000, "primary_task": "General Reasoning & Chat",
        "context_window": "2K tokens", "license": "Apache 2.0",
        "family": "falcon", "generation": 1, "predecessor": None, "successor": None,
        "huggingface_url": "https://huggingface.co/tiiuae/falcon-7b-instruct",
        "description": "TII's Falcon-7B, one of the first truly open 7B-class models to compete with proprietary alternatives. Trained on 1.5T tokens of the RefinedWeb corpus. While surpassed by newer models in raw benchmarks, it remains a historically significant and fully Apache 2.0 licensed model for research and deployment.",
        "badges": ["verified"], "hardware_compat": {"raspberry_pi_5": False, "mobile_phone": False, "consumer_gpu_8gb": True, "consumer_gpu_24gb": True, "cpu_only": True, "apple_silicon_16gb": True, "min_ram_gb_q4": 4.2, "recommended_backend": "llama.cpp"},
        "tags": ["chat", "reasoning", "multilingual", "open-source"]
    }),
]

DATASETS = [
    ("gsm8k", {
        "name": "GSM8K", "creator": "OpenAI", "size_rows": "8,792",
        "target_task": "Math Reasoning", "license": "MIT",
        "huggingface_url": "https://huggingface.co/datasets/gsm8k",
        "description": "The standard benchmark for grade-school math word problems. 8.8K linguistically diverse problems requiring multi-step arithmetic reasoning. Each problem includes a step-by-step natural language solution. The de facto evaluation standard for math reasoning in language models.",
        "tags": ["math-reasoning", "evaluation", "benchmark", "chain-of-thought"]
    }),
    ("openmathreasoning", {
        "name": "OpenMathReasoning", "creator": "NVIDIA", "size_rows": "4,920,000",
        "target_task": "Math Reasoning", "license": "CC-BY-4.0",
        "huggingface_url": "https://huggingface.co/datasets/nvidia/OpenMathReasoning",
        "description": "NVIDIA's massive 4.9M-row math reasoning dataset with chain-of-thought solutions. Covers a wide range of difficulty levels from arithmetic to competition math. Designed for teaching models to reason step-by-step through mathematical problems. Complements OpenMathInstruct-2 for comprehensive math fine-tuning.",
        "tags": ["math-reasoning", "chain-of-thought", "fine-tuning", "synthetic-data", "large-scale"]
    }),
    ("numina-math-cot", {
        "name": "NuminaMath-CoT", "creator": "AI-MO (Numina)", "size_rows": "859,000",
        "target_task": "Math Reasoning", "license": "Apache 2.0",
        "huggingface_url": "https://huggingface.co/datasets/AI-MO/NuminaMath-CoT",
        "description": "Chain-of-thought math dataset from the team that won the AI Math Olympiad prize. 859K high-quality problems with detailed step-by-step solutions. Covers competition-level mathematics and advanced problem-solving strategies. The gold standard for training SLMs on mathematical reasoning.",
        "tags": ["math-reasoning", "chain-of-thought", "fine-tuning", "competition-math"]
    }),
    ("metamathqa", {
        "name": "MetaMathQA", "creator": "meta-math", "size_rows": "395,000",
        "target_task": "Math Reasoning", "license": "MIT",
        "huggingface_url": "https://huggingface.co/datasets/meta-math/MetaMathQA",
        "description": "395K bootstrapped math questions generated by rewriting GSM8K and MATH problems from multiple perspectives. Trains models to approach the same problem through different reasoning paths. Proven effective at improving math performance in small models through data augmentation.",
        "tags": ["math-reasoning", "fine-tuning", "synthetic-data", "chain-of-thought"]
    }),
    ("codefeedback-filtered-instruction", {
        "name": "CodeFeedback-Filtered-Instruction", "creator": "m-a-p", "size_rows": "156,868",
        "target_task": "Code Generation", "license": "MIT",
        "huggingface_url": "https://huggingface.co/datasets/m-a-p/CodeFeedback-Filtered-Instruction",
        "description": "A filtered and decontaminated code instruction dataset combining the best of Magicoder, ShareGPT code conversations, and Evol-Instruct code problems. 157K high-quality coding tasks with verified solutions across multiple programming languages. MIT licensed for unrestricted use.",
        "tags": ["code-generation", "fine-tuning", "decontaminated", "multi-language", "instruction-tuning"]
    }),
    ("self-oss-instruct-sc2", {
        "name": "self-oss-instruct-sc2-exec-filter-50k", "creator": "bigcode", "size_rows": "50,722",
        "target_task": "Code Generation", "license": "Apache 2.0",
        "huggingface_url": "https://huggingface.co/datasets/bigcode/self-oss-instruct-sc2-exec-filter-50k",
        "description": "Self-instruction dataset from the StarCoder2 project with execution-based filtering. 50K high-quality coding problems where generated solutions were verified by actually running the code. Produced during the training of StarCoder2, one of the best open code models.",
        "tags": ["code-generation", "fine-tuning", "execution-verified", "instruction-tuning"]
    }),
    ("opc-sft-stage2", {
        "name": "opc-sft-stage2", "creator": "OpenCoder", "size_rows": "436,000",
        "target_task": "Code Generation", "license": "Apache 2.0",
        "huggingface_url": "https://huggingface.co/datasets/OpenCoder/opc-sft-stage2",
        "description": "Stage 2 supervised fine-tuning dataset from the OpenCoder project. 436K examples used to train open-source code models. Covers diverse programming tasks, languages, and difficulty levels. Part of a fully open code model training pipeline.",
        "tags": ["code-generation", "fine-tuning", "multi-language", "instruction-tuning", "large-scale"]
    }),
    ("oasst2", {
        "name": "OpenAssistant Conversations (oasst2)", "creator": "LAION", "size_rows": "135,000",
        "target_task": "Instruction Following", "license": "Apache 2.0",
        "huggingface_url": "https://huggingface.co/datasets/OpenAssistant/oasst2",
        "description": "Human-generated multi-turn conversation trees from the OpenAssistant project. 135K messages across 66K conversation trees in multiple languages. Each message is labeled for quality, making it ideal for curated instruction tuning. A foundational open-source alternative to proprietary RLHF data.",
        "tags": ["instruction-following", "chat", "fine-tuning", "human-generated", "multilingual"]
    }),
    ("lmsys-chat-1m", {
        "name": "lmsys-chat-1m", "creator": "LMSYS", "size_rows": "1,000,000",
        "target_task": "Instruction Following", "license": "Apache 2.0",
        "huggingface_url": "https://huggingface.co/datasets/lmsys/lmsys-chat-1m",
        "description": "One million real user conversations with 25+ LLMs from Chatbot Arena. Contains diverse prompts, model responses, and human preference votes. Invaluable for understanding real-world usage patterns and training models to handle the full diversity of user requests.",
        "tags": ["instruction-following", "chat", "fine-tuning", "human-feedback", "large-scale"]
    }),
    ("wildchat-1m", {
        "name": "WildChat-1M", "creator": "Allen Institute for AI", "size_rows": "1,040,000",
        "target_task": "Instruction Following", "license": "ODC-BY",
        "huggingface_url": "https://huggingface.co/datasets/allenai/WildChat-1M",
        "description": "Over 1M real conversations between users and GPT-3.5/GPT-4. Captures the genuine distribution of user requests — from coding to creative writing to roleplay. A critical resource for training models that handle the messy, diverse reality of user interactions.",
        "tags": ["instruction-following", "chat", "fine-tuning", "human-generated", "large-scale"]
    }),
    ("wikisql", {
        "name": "WikiSQL", "creator": "Salesforce Research", "size_rows": "80,654",
        "target_task": "Text-to-SQL Generation", "license": "BSD",
        "huggingface_url": "https://huggingface.co/datasets/wikisql",
        "description": "The original text-to-SQL benchmark. 80K examples pairing natural language questions with SQL queries over Wikipedia tables. Simpler than Spider (single-table queries only) but larger and ideal for initial fine-tuning before moving to more complex multi-table tasks.",
        "tags": ["text-to-sql", "benchmark", "fine-tuning", "structured-data"]
    }),
    ("squad-v2", {
        "name": "SQuAD v2", "creator": "Stanford", "size_rows": "151,574",
        "target_task": "Extractive Question Answering", "license": "CC-BY-SA-4.0",
        "huggingface_url": "https://huggingface.co/datasets/rajpurkar/squad_v2",
        "description": "The Stanford Question Answering Dataset v2 — the standard for reading comprehension evaluation. 150K+ questions over Wikipedia articles, including unanswerable questions that test a model's ability to know when it doesn't know. Essential for training and evaluating QA capabilities.",
        "tags": ["knowledge-qa", "evaluation", "benchmark", "reading-comprehension"]
    }),
    ("conll2003", {
        "name": "CoNLL-2003", "creator": "CoNLL Shared Task", "size_rows": "20,744",
        "target_task": "Named Entity Recognition", "license": "CC-BY-4.0",
        "huggingface_url": "https://huggingface.co/datasets/conll2003",
        "description": "The classic NER benchmark dataset. 20K sentences annotated with four entity types: PERSON, ORGANIZATION, LOCATION, and MISC. The standard evaluation set for named entity recognition in English. Simple, well-understood, and ideal for fine-tuning small models on NER.",
        "tags": ["named-entity-recognition", "benchmark", "evaluation", "fine-tuning"]
    }),
    ("opus-100", {
        "name": "OPUS-100", "creator": "Helsinki-NLP", "size_rows": "1,000,000",
        "target_task": "Machine Translation", "license": "CC-BY-4.0",
        "huggingface_url": "https://huggingface.co/datasets/opus100",
        "description": "A multilingual translation corpus covering 100 languages with English-centric parallel data. 1M sentence pairs across diverse language families. Ideal for fine-tuning small models on translation tasks for low-resource language pairs.",
        "tags": ["translation", "multilingual", "fine-tuning", "large-scale"]
    }),
]

TASKS = [
    ("text-summarization", {
        "task_id": "text-summarization", "display_name": "Text Summarization",
        "domain": "Natural Language Processing",
        "description": "Condensing long documents, articles, or conversations into shorter summaries while preserving key information and meaning. Tests a model's ability to identify salient content, maintain factual accuracy, and produce fluent compressed text.",
        "input_format": "Long-form text (article, document, dialogue transcript)",
        "output_format": "Concise summary capturing essential information",
        "metrics_tracked": ["ROUGE-L", "BERTScore", "Factual Consistency"],
        "recommended_models": [
            {"ref": "models/qwen3-5-4b.yaml", "notes": "256K context ideal for long-document summarization."},
            {"ref": "models/phi-3.5-mini-instruct.yaml", "notes": "128K context, MIT licensed, strong at concise generation."},
            {"ref": "models/smollm3-3b.yaml", "notes": "Fully open, dual-mode reasoning for extractive and abstractive summarization."}
        ],
        "recommended_datasets": [
            {"ref": "datasets/smoltalk.yaml", "purpose": "general-instruction-base"}
        ],
        "related_tasks": [
            {"task_id": "instruction-following", "relationship": "parent"},
            {"task_id": "knowledge-qa", "relationship": "related"}
        ]
    }),
    ("named-entity-recognition", {
        "task_id": "named-entity-recognition", "display_name": "Named Entity Recognition (NER)",
        "domain": "Natural Language Processing",
        "description": "Identifying and classifying named entities (persons, organizations, locations, dates, etc.) in unstructured text. A foundational NLP task critical for information extraction, knowledge graph construction, and document understanding pipelines.",
        "input_format": "Raw text passage",
        "output_format": "Token-level entity labels (e.g., PER, ORG, LOC, MISC)",
        "metrics_tracked": ["F1 Score (Entity-level)", "Precision", "Recall"],
        "recommended_models": [
            {"ref": "models/granite-3-2-2b-instruct.yaml", "notes": "Strong structured output, ideal for entity extraction at 2B."},
            {"ref": "models/qwen2.5-0.5b-instruct.yaml", "notes": "Surprisingly capable at NER despite tiny size — great for lightweight extraction."},
            {"ref": "models/smollm2-1.7b-instruct.yaml", "notes": "Fully open, strong at structured extraction tasks."}
        ],
        "recommended_datasets": [
            {"ref": "datasets/conll2003.yaml", "purpose": "fine-tuning"}
        ],
        "related_tasks": [
            {"task_id": "instruction-following", "relationship": "parent"},
            {"task_id": "knowledge-qa", "relationship": "related"}
        ]
    }),
    ("machine-translation", {
        "task_id": "machine-translation", "display_name": "Machine Translation",
        "domain": "Multilingual NLP",
        "description": "Translating text from one language to another while preserving meaning, tone, and nuance. Tests cross-lingual understanding and generation. Critical for making AI accessible across language communities.",
        "input_format": "Source language text + target language specification",
        "output_format": "Fluent translation in the target language",
        "metrics_tracked": ["BLEU", "COMET", "chrF"],
        "recommended_models": [
            {"ref": "models/qwen3-5-4b.yaml", "notes": "100+ languages, state-of-the-art multilingual translation at 4B."},
            {"ref": "models/qwen2.5-7b-instruct.yaml", "notes": "29+ languages with strong cross-lingual understanding."},
            {"ref": "models/phi-3.5-mini-instruct.yaml", "notes": "Significantly improved multilingual over Phi-3-mini, MIT licensed."}
        ],
        "recommended_datasets": [
            {"ref": "datasets/opus100.yaml", "purpose": "fine-tuning"}
        ],
        "related_tasks": [
            {"task_id": "instruction-following", "relationship": "parent"},
            {"task_id": "multimodal-reasoning", "relationship": "related"}
        ]
    }),
    ("extractive-qa", {
        "task_id": "extractive-qa", "display_name": "Extractive Question Answering",
        "domain": "Information Retrieval & QA",
        "description": "Reading a passage and extracting the exact answer span for a given question. Unlike knowledge QA (which relies on memorized facts), extractive QA tests reading comprehension — the answer must be found in the provided text. Fundational for RAG pipelines.",
        "input_format": "Context passage + question",
        "output_format": "Answer span extracted verbatim from the context",
        "metrics_tracked": ["Exact Match", "F1 Score"],
        "recommended_models": [
            {"ref": "models/phi-4-mini-instruct.yaml", "notes": "Strong reading comprehension, ideal for RAG pipelines."},
            {"ref": "models/qwen3-5-4b.yaml", "notes": "Long context support enables processing lengthy passages."},
            {"ref": "models/smollm3-3b.yaml", "notes": "Fully open, good baseline for RAG research."}
        ],
        "recommended_datasets": [
            {"ref": "datasets/squad-v2.yaml", "purpose": "evaluation"}
        ],
        "related_tasks": [
            {"task_id": "knowledge-qa", "relationship": "related"},
            {"task_id": "instruction-following", "relationship": "parent"}
        ]
    }),
    ("sentiment-analysis", {
        "task_id": "sentiment-analysis", "display_name": "Sentiment Analysis",
        "domain": "Natural Language Processing",
        "description": "Classifying the sentiment or emotional tone of text — positive, negative, neutral, or fine-grained emotions. A bread-and-butter NLP task used in customer feedback analysis, social media monitoring, and brand intelligence. Well-suited to small, specialized models.",
        "input_format": "Text passage (review, tweet, comment)",
        "output_format": "Sentiment label with optional confidence score",
        "metrics_tracked": ["Accuracy", "F1 Score", "Macro-F1"],
        "recommended_models": [
            {"ref": "models/smollm2-135m-instruct.yaml", "notes": "Tiny 135M model sufficient for sentiment classification when fine-tuned."},
            {"ref": "models/qwen2.5-0.5b-instruct.yaml", "notes": "Minimal resource requirements, strong at text classification."},
            {"ref": "models/tinyllama-1-1b.yaml", "notes": "Good baseline with strong text understanding at 1.1B."}
        ],
        "recommended_datasets": [],
        "related_tasks": [
            {"task_id": "named-entity-recognition", "relationship": "related"},
            {"task_id": "instruction-following", "relationship": "parent"}
        ]
    }),
]


def write_yaml(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)


def main():
    print(f"Adding {len(MODELS)} models, {len(DATASETS)} datasets, {len(TASKS)} tasks...\n")

    added = {"models": 0, "datasets": 0, "tasks": 0}
    skipped = {"models": 0, "datasets": 0, "tasks": 0}

    for fname, data in MODELS:
        path = ROOT / "models" / f"{fname}.yaml"
        if path.exists():
            skipped["models"] += 1
            print(f"  SKIP (exists): models/{fname}.yaml")
        else:
            write_yaml(path, data)
            added["models"] += 1
            print(f"  ADD: models/{fname}.yaml — {data['name']} ({data['parameters']})")

    for fname, data in DATASETS:
        path = ROOT / "datasets" / f"{fname}.yaml"
        if path.exists():
            skipped["datasets"] += 1
            print(f"  SKIP (exists): datasets/{fname}.yaml")
        else:
            write_yaml(path, data)
            added["datasets"] += 1
            print(f"  ADD: datasets/{fname}.yaml — {data['name']} ({data['size_rows']} rows)")

    for fname, data in TASKS:
        path = ROOT / "tasks" / f"{fname}.yaml"
        if path.exists():
            skipped["tasks"] += 1
            print(f"  SKIP (exists): tasks/{fname}.yaml")
        else:
            write_yaml(path, data)
            added["tasks"] += 1
            print(f"  ADD: tasks/{fname}.yaml — {data['display_name']}")

    print(f"\nDone: +{added['models']} models, +{added['datasets']} datasets, +{added['tasks']} tasks")
    if skipped["models"] or skipped["datasets"] or skipped["tasks"]:
        print(f"Skipped: {skipped['models']} models, {skipped['datasets']} datasets, {skipped['tasks']} tasks (already exist)")


if __name__ == "__main__":
    main()
