# CtxOS Cookbook Engine

Convert Declarative AI Recipes → Executable Infrastructure

## 🧠 Philosophy

This repo is an AI DevOps compiler that transforms YAML recipes into executable Jupyter notebooks, Docker configurations, and deployment manifests. It is NOT just a notebook generator.

## 🏗 Structure

```
CtxOS/cookbook/
│
├── cookbooks/                # Declarative recipes
│   ├── llm_finetune.yaml
│   ├── rag_pipeline.yaml
│   └── agent_builder.yaml
│
├── ctxcook/                  # Core engine (Python package)
│   ├── __init__.py
│   ├── parser.py
│   ├── validator.py
│   ├── generator.py
│   ├── notebook.py
│   ├── exporter.py
│   └── cli.py
│
├── templates/
│   ├── colab_template.ipynb
│   ├── docker_template.j2
│   └── hf_deploy_template.j2
│
├── tests/
│   ├── test_parser.py
│   └── test_validator.py
│
├── pyproject.toml
├── README.md
└── Makefile
```

## 🚀 Quick Start

### Installation

```bash
# Install locally
pip install -e .
```

This makes the `ctxcook` CLI available globally.

### Usage

```bash
# Build a notebook from a recipe
ctxcook build cookbooks/llm_finetune.yaml --output notebooks/finetune.ipynb

# Help
ctxcook --help
ctxcook build --help
```

## 📖 Example Recipes

### LLM Fine-tuning Recipe

```yaml
name: llm_finetune_basic

model:
  base: mistralai/Mistral-7B-v0.1
  quantization: 4bit

dataset:
  source: huggingface
  name: secpatch/train
```

### RAG Pipeline Recipe

```yaml
name: rag_pipeline_basic

model:
  base: sentence-transformers/all-MiniLM-L6-v2
  type: embedding

dataset:
  source: local
  path: ./documents

retrieval:
  chunk_size: 512
  overlap: 50
```

### Agent Builder Recipe

```yaml
name: agent_builder_basic

model:
  base: gpt-3.5-turbo
  provider: openai

tools:
  - name: calculator
    type: function
  - name: web_search
    type: api

agent:
  type: conversational
  memory: true
```

## 🔧 Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

```bash
black ctxcook/
flake8 ctxcook/
```

## 🚀 Production Upgrade Plan

### Phase 1
- [x] Add Jinja2 templating
- [x] Add environment config (Colab / Docker / Local)
- [x] Add version pinning

### Phase 2
- [ ] DAG builder (convert recipe → pipeline graph)
- [ ] Add cost estimation
- [ ] Add GPU selection logic

### Phase 3
- [ ] Integrate with CtxAI runtime
- [ ] Allow prompt → auto-generate cookbook YAML
- [ ] Add marketplace registry support

## 📄 License

MIT License - see LICENSE file for details.
