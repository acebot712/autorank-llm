# AutoRank-LLM

AutoRank-LLM is an innovative Python package designed to automatically evaluate and rank Language Learning Models (LLMs) without human intervention. It utilizes a recursive peer review system with adaptive weighting to provide a fair and dynamic ranking of LLMs based on their performance on language understanding and generation tasks.

## Features

- **Recursive Evaluation**: LLMs evaluate each other in multiple rounds to establish a performance-based ranking.
- **Adaptive Weighting**: Evaluations are weighted by the evaluator's current ranking to ensure that more skilled LLMs have a greater influence.
- **Dynamic Adjustment**: Rankings are updated after each round based on weighted evaluations, allowing for gradual stabilization of the system.
- **Normalization and Scaling**: Techniques applied to prevent score inflation/deflation and maintain a consistent ranking scale.
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

Here's a simple example:
```python
from autorank_llm.evaluator import LLMEvaluator

# Define the model names and the task
model_names = ["mistral:instruct", "orca-mini", "llama2"]
task = "3 names of a pet cow."

# Create an evaluator instance
evaluator = LLMEvaluator(model_names, task)

# Perform the evaluation
evaluator.evaluate_llms()

# Retrieve and display the rankings
rankings = evaluator.get_rankings()
print(rankings)
```

Only [Ollama models](https://ollama.ai/library) are supported for now.

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
