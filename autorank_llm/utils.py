# utils.py
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def normalize_skill_levels(llms: List[Any]) -> None:
    """
    Normalize the skill levels of LLM instances to a 0-100 scale.
    :param llms: List of LLM instances.
    :raises ValueError: If input is invalid.
    """
    if not llms or not isinstance(llms, list):
        raise ValueError("The list of LLMs is empty or not a list.")
    skill_levels = [llm.skill_level for llm in llms]
    min_skill, max_skill = min(skill_levels), max(skill_levels)
    for llm in llms:
        # Protect against division by zero
        if max_skill != min_skill:
            llm.skill_level = 100 * (llm.skill_level - min_skill) / (max_skill - min_skill)
        else:
            llm.skill_level = 50

def rank_llms(llms: List[Any]) -> List[Any]:
    """
    Rank LLM instances based on their skill levels.
    :param llms: List of LLM instances.
    :return: List of LLM instances sorted by skill level in descending order.
    :raises ValueError: If input is invalid.
    """
    if not llms or not isinstance(llms, list):
        raise ValueError("The list of LLMs is empty or not a list.")
    sorted_llms = sorted(llms, key=lambda x: x.skill_level, reverse=True)
    logger.info("Final Ranking of LLMs:")
    for rank, llm in enumerate(sorted_llms, start=1):
        logger.info(f"Rank {rank}: {llm.name} with skill level {llm.skill_level:.2f}")
    return sorted_llms

# Explainability, fairness, and robustness utilities

def explainability_report(logs: List[Dict[str, Any]]) -> str:
    """
    Generate a human-readable explainability report from logs.
    :param logs: List of explainability log dicts.
    :return: String report.
    """
    report = ["Explainability Report:"]
    for entry in logs:
        report.append(
            f"Iteration {entry['iteration']}: {entry['evaluator']} evaluated {entry['evaluatee']} on task '{entry['task']}'\n"
            f"  Response: {entry['response']}\n  Score: {entry['score']}  Weighted: {entry['weighted_score']}"
        )
    return '\n'.join(report)

def check_bias_and_fairness(llms: List[Any], logs: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Bias and fairness analysis (future feature).

    :param llms: List of LLM instances.
    :param logs: List of evaluation logs.
    :return: Dict with bias/fairness metrics.
    :raises NotImplementedError: This feature is not yet implemented
    """
    raise NotImplementedError(
        "Bias and fairness analysis is planned for a future release. "
        "Follow https://github.com/acebot712/autorank-llm for updates."
    )

def check_robustness(llms: List[Any], logs: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Robustness analysis (future feature).

    :param llms: List of LLM instances.
    :param logs: List of evaluation logs.
    :return: Dict with robustness metrics.
    :raises NotImplementedError: This feature is not yet implemented
    """
    raise NotImplementedError(
        "Robustness analysis is planned for a future release. "
        "Follow https://github.com/acebot712/autorank-llm for updates."
    )

def generate_challenges(llm: Any, num_challenges: int = 5, topic: str = "general") -> List[str]:
    """
    Automated challenge/task generation (future feature).

    :param llm: An LLM instance to generate tasks.
    :param num_challenges: Number of challenges to generate.
    :param topic: Topic or domain for the challenges.
    :return: List of generated challenge strings.
    :raises NotImplementedError: This feature is not yet implemented
    """
    raise NotImplementedError(
        "Automated challenge generation is planned for a future release. "
        "Follow https://github.com/acebot712/autorank-llm for updates."
    )
