import logging
from typing import List, Dict, Any, Optional
from .models import LLM, LLMEvaluationHelper
from .utils import normalize_skill_levels, rank_llms

# Set up a specific logger for this module
logger = logging.getLogger(__name__)


class PluginManager:
    """
    Manages plugins for custom evaluation tasks or metrics.
    """
    def __init__(self) -> None:
        self.plugins: List[Any] = []

    def register(self, plugin: Any) -> None:
        self.plugins.append(plugin)

    def run(self, *args, **kwargs) -> List[Any]:
        results = []
        for plugin in self.plugins:
            if hasattr(plugin, 'run'):
                results.append(plugin.run(*args, **kwargs))
            else:
                results.append(plugin(*args, **kwargs))
        return results


class EvaluationLogger:
    """
    Handles explainability, fairness, and robustness logs.
    """
    def __init__(self) -> None:
        self.explainability_log: List[Dict[str, Any]] = []
        self.fairness_log: List[Any] = []
        self.robustness_log: List[Any] = []

    def log_explainability(self, entry: Dict[str, Any]) -> None:
        self.explainability_log.append(entry)

    def get_logs(self) -> Dict[str, Any]:
        return {
            'explainability_log': self.explainability_log,
            'fairness_log': self.fairness_log,
            'robustness_log': self.robustness_log
        }


class LLMEvaluator:
    """
    Orchestrates the evaluation and ranking of LLMs.
    """
    def __init__(self, model_configs: List[Dict[str, Any]], task: str, threshold: float = 0.5, debug: bool = False) -> None:
        """
        :param model_configs: List of dicts, each with 'name', 'model_name', and 'backend'.
        :param task: The task to be performed by the LLMs.
        :param threshold: The convergence threshold for the evaluation process.
        :param debug: Flag to run in debug mode.
        :raises ValueError: If input is invalid.
        """
        if not isinstance(model_configs, list) or not model_configs:
            raise ValueError("model_configs must be a non-empty list of dicts.")
        for cfg in model_configs:
            if not isinstance(cfg, dict) or 'name' not in cfg or 'model_name' not in cfg:
                raise ValueError("Each model config must be a dict with 'name' and 'model_name'.")
        if not task or not isinstance(task, str):
            raise ValueError("task must be a non-empty string.")
        self.model_configs: List[Dict[str, Any]] = model_configs
        self.task: str = task
        self.threshold: float = threshold
        self.debug: bool = debug
        self.llms: List[LLM] = [LLM(cfg['name'], cfg['model_name'], cfg.get('backend', 'ollama')) for cfg in model_configs]
        self.logger: EvaluationLogger = EvaluationLogger()
        self.plugin_manager: PluginManager = PluginManager()

    def evaluate_llms(self) -> Dict[str, Any]:
        """
        Evaluate and rank the LLMs based on their performance on the specified task.
        :return: Dictionary with rankings and logs.
        """
        converged = False
        iteration = 0

        while not converged:
            iteration += 1
            max_change = 0.0

            try:
                for evaluator in self.llms:
                    for evaluatee in self.llms:
                        if evaluator != evaluatee:
                            task_response = evaluatee.perform_task(self.task)
                            if task_response:
                                score = LLMEvaluationHelper.evaluate(evaluator, self.task, task_response)
                                weighted_score = score * evaluator.skill_level
                                evaluatee.evaluations.append(weighted_score)
                                # Explainability hook
                                self.logger.log_explainability({
                                    'iteration': iteration,
                                    'evaluator': evaluator.name,
                                    'evaluatee': evaluatee.name,
                                    'task': self.task,
                                    'response': task_response,
                                    'score': score,
                                    'weighted_score': weighted_score
                                })
                                # Fairness/robustness hooks (placeholder)
                                # self.logger.fairness_log.append(...)
                                # self.logger.robustness_log.append(...)

                # Normalize skill levels
                normalize_skill_levels(self.llms)

                # Check for convergence
                changes = [LLMEvaluationHelper.update_skill_level(llm) for llm in self.llms]
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
        # Optionally return explainability/fairness/robustness logs
        logs = self.logger.get_logs()
        return {
            'rankings': self.llms,
            **logs
        }

    def register_plugin(self, plugin: Any) -> None:
        self.plugin_manager.register(plugin)

    def run_plugins(self, *args, **kwargs) -> List[Any]:
        return self.plugin_manager.run(*args, **kwargs)

    def enable_distributed(self, cluster_config: Optional[Dict[str, Any]] = None) -> None:
        """
        Enable distributed evaluation (future feature).

        :param cluster_config: Configuration for distributed cluster
        :raises NotImplementedError: This feature is not yet implemented
        """
        raise NotImplementedError(
            "Distributed evaluation is planned for a future release. "
            "Follow https://github.com/acebot712/autorank-llm for updates."
        )

    def get_dashboard_data(self) -> Dict[str, Any]:
        logs = self.logger.get_logs()
        return {
            'rankings': [llm.name for llm in self.llms],
            **logs,
            'plugin_results': self.run_plugins()
        }

