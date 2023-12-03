# utils.py
import logging

logger = logging.getLogger(__name__)

def normalize_skill_levels(llms):
    """
    Normalize the skill levels of LLM instances to a 0-100 scale.

    :param llms: List of LLM instances.
    """
    if not llms:
        raise ValueError("The list of LLMs is empty.")
        
    skill_levels = [llm.skill_level for llm in llms]
    min_skill, max_skill = min(skill_levels), max(skill_levels)
    for llm in llms:
        # Protect against division by zero
        if max_skill != min_skill:
            llm.skill_level = 100 * (llm.skill_level - min_skill) / (max_skill - min_skill)
        else:
            llm.skill_level = 50

def rank_llms(llms):
    """
    Rank LLM instances based on their skill levels.

    :param llms: List of LLM instances.
    :return: List of LLM instances sorted by skill level in descending order.
    """
    if not llms:
        raise ValueError("The list of LLMs is empty.")
        
    sorted_llms = sorted(llms, key=lambda x: x.skill_level, reverse=True)
    logger.info("Final Ranking of LLMs:")
    for rank, llm in enumerate(sorted_llms, start=1):
        logger.info(f"Rank {rank}: {llm.name} with skill level {llm.skill_level:.2f}")
    return sorted_llms
