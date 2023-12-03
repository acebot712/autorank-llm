from autorank_llm.evaluator import LLMEvaluator

# User-defined model names and task
model_names = ["mistral:instruct", "orca-mini", "llama2"]
task = "3 names for a pet cow"

# Create evaluator instance
evaluator = LLMEvaluator(model_names, task, debug=True)

# Perform evaluation
evaluator.evaluate_llms()

# Get rankings
rankings = evaluator.get_rankings()
print(rankings)
