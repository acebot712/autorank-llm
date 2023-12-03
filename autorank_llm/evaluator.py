import logging
from .models import LLM
from .utils import normalize_skill_levels, rank_llms

# Set up a specific logger for this module
logger = logging.getLogger(__name__)

class LLMEvaluator:
    """
    A class to evaluate and rank a group of Language Learning Models (LLMs).

    Attributes:
        model_names (list): A list of model names to be evaluated.
        task (str): The task for the LLMs to perform.
        threshold (float): The convergence threshold for the evaluation process.
        debug (bool): Flag to run in debug mode which runs the evaluation only once.
        llms (list): A list of LLM instances.
    """

    def __init__(self, model_names, task, threshold=0.5, debug=False):
        """
        Initialize the LLMEvaluator with a set of model names and a task.

        :param model_names: A list of model names for the LLMs.
        :param task: The task to be performed by the LLMs.
        :param threshold: The convergence threshold for the evaluation process.
        :param debug: Flag to run in debug mode.
        """
        self.model_names = model_names
        self.task = task
        self.threshold = threshold
        self.debug = debug
        self.llms = [LLM(f"LLM{i+1}", model_name) for i, model_name in enumerate(model_names)]

    def evaluate_llms(self):
        """
        Evaluate and rank the LLMs based on their performance on the specified task.
        """
        converged = False
        iteration = 0

        while not converged:
            iteration += 1
            max_change = 0

            try:
                for evaluator in self.llms:
                    for evaluatee in self.llms:
                        if evaluator != evaluatee:
                            task_response = evaluatee.perform_task(self.task)
                            if task_response:
                                score = evaluator.evaluate(self.task, task_response)
                                weighted_score = score * evaluator.skill_level
                                evaluatee.evaluations.append(weighted_score)

                # Normalize skill levels
                normalize_skill_levels(self.llms)

                # Check for convergence
                changes = [llm.update_skill_level() for llm in self.llms]
                max_change = max(changes)
                converged = max_change < self.threshold or self.debug

                if self.debug:
                    logger.info(f"Debug mode: Completed iteration {iteration}")
                    break

            except Exception as e:
                logger.exception("An error occurred during the evaluation process: %s", e)
                break

        # Rank the LLMs based on their final skill levels
        rank_llms(self.llms)

