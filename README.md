# AutoRank-LLM

[![CI](https://github.com/acebot712/autorank-llm/actions/workflows/ci.yml/badge.svg)](https://github.com/acebot712/autorank-llm/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

AutoRank-LLM is a Python package that automatically evaluates and ranks Language Learning Models (LLMs) using a recursive peer review system. Models evaluate each other's responses, with rankings dynamically adjusted based on weighted evaluations until convergence.

## Key Features

- **Recursive Peer Evaluation**: LLMs evaluate each other iteratively to establish performance-based rankings
- **Adaptive Weighting**: Evaluations are weighted by the evaluator's current skill level
- **Multi-Backend Support**: Works with Ollama, OpenAI, HuggingFace, and custom backends
- **Explainable Rankings**: Complete audit trail of all evaluations and ranking decisions
- **Plugin System**: Extensible architecture for custom evaluation tasks and metrics

## Installation

```bash
pip install autorank-llm
```

For local development:

```bash
git clone https://github.com/acebot712/autorank-llm.git
cd autorank-llm
pip install -e .
```

### Backend-Specific Installation

```bash
# For Ollama
pip install langchain-community

# For OpenAI
pip install langchain-openai

# For HuggingFace
pip install langchain-huggingface
```

## Quick Start

```python
from autorank_llm import LLMEvaluator

# Define models to evaluate
model_configs = [
    {"name": "mistral", "model_name": "mistral:instruct", "backend": "ollama"},
    {"name": "orca-mini", "model_name": "orca-mini", "backend": "ollama"},
    {"name": "llama2", "model_name": "llama2", "backend": "ollama"},
]

# Create evaluator and run
evaluator = LLMEvaluator(model_configs, task="Name 3 pets for a cow")
results = evaluator.evaluate_llms()

# Display rankings
for i, llm in enumerate(results['rankings'], 1):
    print(f"Rank {i}: {llm.name} (Skill: {llm.skill_level:.2f})")
```

## How It Works

1. **Initialization**: Each LLM starts with a random skill level (50-100)
2. **Task Execution**: Each model performs the specified task
3. **Cross-Evaluation**: Every model evaluates every other model's response
4. **Weighted Scoring**: Evaluations are weighted by the evaluator's current skill level
5. **Skill Update**: Each model's skill level is updated based on received evaluations
6. **Normalization**: Skill levels are normalized to a 0-100 scale
7. **Convergence Check**: Process repeats until skill levels stabilize

## Advanced Usage

### Explainability Reports

```python
from autorank_llm import explainability_report

results = evaluator.evaluate_llms()
report = explainability_report(results['explainability_log'])
print(report)
```

### Custom Plugin System

```python
class CustomMetricPlugin:
    def run(self, *args, **kwargs):
        return {'custom_metric': 42}

evaluator.register_plugin(CustomMetricPlugin())
plugin_results = evaluator.run_plugins()
```

### Using Different Backends

```python
# OpenAI
model_configs = [
    {"name": "gpt-3.5", "model_name": "gpt-3.5-turbo", "backend": "openai"},
]

# HuggingFace
model_configs = [
    {"name": "llama", "model_name": "meta-llama/Llama-2-7b-hf", "backend": "huggingface"},
]
```

## API Reference

### `LLMEvaluator`

**Constructor:**
```python
LLMEvaluator(model_configs, task, threshold=0.5, debug=False)
```

- `model_configs`: List of dicts with 'name', 'model_name', and 'backend'
- `task`: String description of the task for LLMs to perform
- `threshold`: Convergence threshold (default: 0.5)
- `debug`: If True, runs only one iteration (default: False)

**Methods:**
- `evaluate_llms()`: Run evaluation and return results dict
- `register_plugin(plugin)`: Register a custom plugin
- `run_plugins()`: Execute all registered plugins
- `get_dashboard_data()`: Get data formatted for dashboards/APIs

## Testing

Run the test suite:

```bash
python -m unittest discover tests
```

## Roadmap

Future features being considered:

- Distributed evaluation across multiple nodes
- Automated bias and fairness analysis
- Robustness testing framework
- LLM-generated challenge tasks
- Web dashboard for visualization

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with clear commit messages
4. Ensure tests pass (`python -m unittest discover tests`)
5. Follow PEP 8 style guidelines
6. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Citation

If you use AutoRank-LLM in your research, please cite:

```bibtex
@software{autorank_llm,
  author = {Sarkar, Abhijoy},
  title = {AutoRank-LLM: Automated Ranking of Language Learning Models},
  year = {2024},
  url = {https://github.com/acebot712/autorank-llm}
}
```

## Acknowledgments

Inspired by the need for fair, unbiased, and automated evaluation of the growing number of LLMs. Thanks to the open-source community for their contributions.

---

**Note**: This project is under active development. APIs may change between versions. Check the [CHANGELOG](CHANGELOG.md) for updates.
