from autorank_llm import LLMEvaluator

# Define the model configs (name, model_name, backend)
model_configs = [
    {"name": "mistral", "model_name": "mistral:instruct", "backend": "ollama"},
    {"name": "orca-mini", "model_name": "orca-mini", "backend": "ollama"},
    {"name": "llama2", "model_name": "llama2", "backend": "ollama"},
]
task = "3 names for a pet cow"

# Create evaluator instance
evaluator = LLMEvaluator(model_configs, task, debug=True)

# Perform evaluation
results = evaluator.evaluate_llms()

# Get rankings
rankings = results['rankings']
for i, llm in enumerate(rankings, 1):
    print(f"Rank {i}: {llm.name} (Skill: {llm.skill_level:.2f})")
