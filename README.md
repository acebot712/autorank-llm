# AutoRank-LLM

AutoRank-LLM is an innovative Python package designed to automatically evaluate and rank Language Learning Models (LLMs) without human intervention. It utilizes a recursive peer review system with adaptive weighting to provide a fair and dynamic ranking of LLMs based on their performance on language understanding and generation tasks.

## Features

- **Model-Agnostic Multi-Backend Support**: Evaluate LLMs from Ollama, OpenAI, HuggingFace, and more via a unified interface.
- **Recursive Evaluation**: LLMs evaluate each other in multiple rounds to establish a performance-based ranking.
- **Adaptive Weighting**: Evaluations are weighted by the evaluator's current ranking to ensure that more skilled LLMs have a greater influence.
- **Dynamic Adjustment**: Rankings are updated after each round based on weighted evaluations, allowing for gradual stabilization of the system.
- **Explainable and Auditable Rankings**: Every evaluation and ranking decision is logged for transparency and can be visualized or reported.
- **Robustness, Bias, and Fairness Analysis**: Hooks for automated analysis of model robustness and fairness (extensible for custom checks).
- **Plugin-Based Evaluation Tasks**: Easily add new evaluation tasks or metrics via a plugin system.
- **Scalable and Distributed Evaluation (Pluggable)**: Architecture ready for distributed and parallel evaluation.
- **Machine Learning Integration**: Potential for continuous learning and refinement of the system based on evaluation outcomes.

## Installation

To install AutoRank-LLM, follow these steps:

1. Ensure you have Python 3.6 or higher installed.
2. Clone the repository or download the source code.
3. Navigate to the root directory of the project.
4. Install the package with pip:

```bash
pip install .
```

Or, for a development installation:

```bash
pip install -e .
```

## Usage

To use AutoRank-LLM, you'll need to write a Python script or open a Python shell. 

Here's a simple example with multi-backend support:
```python
from autorank_llm import LLMEvaluator

# Define the model configs (name, model_name, backend)
model_configs = [
    {"name": "mistral", "model_name": "mistral:instruct", "backend": "ollama"},
    {"name": "orca-mini", "model_name": "orca-mini", "backend": "ollama"},
    {"name": "llama2", "model_name": "llama2", "backend": "ollama"},
    # Example for OpenAI or HuggingFace:
    # {"name": "gpt-3.5", "model_name": "gpt-3.5-turbo", "backend": "openai"},
    # {"name": "hf-llama", "model_name": "meta-llama/Llama-2-7b-hf", "backend": "huggingface"},
]
task = "3 names of a pet cow."

evaluator = LLMEvaluator(model_configs, task)
results = evaluator.evaluate_llms()

# Retrieve and display the rankings
rankings = results['rankings']
for i, llm in enumerate(rankings, 1):
    print(f"Rank {i}: {llm.name} (Skill: {llm.skill_level:.2f})")

# Explainability report
from autorank_llm import explainability_report
print(explainability_report(results['explainability_log']))

# Register a plugin for custom evaluation tasks or metrics
class MyCustomPlugin:
    def run(self, *args, **kwargs):
        # Custom logic here
        return {'custom_metric': 42}

evaluator.register_plugin(MyCustomPlugin())
plugin_results = evaluator.run_plugins()
print("Plugin results:", plugin_results)

# Enable distributed evaluation (stub)
evaluator.enable_distributed(cluster_config={"nodes": 4})

# Get data for web dashboard or API
dashboard_data = evaluator.get_dashboard_data()
print("Dashboard data:", dashboard_data)

# Automated challenge/task generation (stub)
from autorank_llm import generate_challenges
challenges = generate_challenges(evaluator.llms[0], num_challenges=3, topic="math reasoning")
print("Generated challenges:", challenges)

# The architecture is extensible for web dashboards, research APIs, and adversarial/diverse task generation.

### Testing

Run unit tests on the package:-  
```sh
python -m unittest discover tests 
```

## Contributing

Contributions to AutoRank-LLM are welcome and greatly appreciated. Here's how you can contribute:

1. **Report Issues**: If you find a bug or have a suggestion for improving the package, please open an issue.
2. **Submit Pull Requests**: Feel free to fork the repository and submit pull requests. Whether it's fixing a bug, adding a feature, or improving documentation, your help is valuable.
3. **Feedback**: Your feedback is crucial to the ongoing improvement of AutoRank-LLM. Share your experiences and ideas for future development.

Please ensure your contributions adhere to the following guidelines:

- Write clear and concise commit messages.
- Make sure your code follows the PEP 8 style guide for Python code.
- Update the documentation to reflect any changes in the API or functionality.
- Add tests for new features to ensure they work as expected.

## License

AutoRank-LLM is released under the [Apache License 2.0](https://github.com/acebot712/autorank-llm/blob/main/LICENSE). Please review the license for more details.

## Acknowledgments

AutoRank-LLM was inspired by the need for a fair and unbiased system to evaluate the burgeoning number of Language Learning Models in the field. We are grateful to the open-source community for their contributions and support.

## Conclusion

AutoRank-LLM offers a robust and scalable solution to the challenge of evaluating and ranking LLMs. By leveraging the collective assessment capabilities of LLMs themselves, it provides a unique approach to understanding and benchmarking language model performance.
