import re
import random
import logging
from typing import Dict, Callable, Optional

# Backend imports (import only if available)
try:
    from langchain.llms import Ollama
except ImportError:
    Ollama = None
try:
    from langchain.llms import OpenAI
except ImportError:
    OpenAI = None
try:
    from langchain.llms import HuggingFaceHub
except ImportError:
    HuggingFaceHub = None

logger = logging.getLogger(__name__)


class ModelRegistry:
    """
    Registry for model backends, allowing model-agnostic LLM support.
    """
    _registry: Dict[str, Callable] = {}

    @classmethod
    def register(cls, backend_name: str, backend_class: Callable) -> None:
        """Register a backend class under a given name."""
        cls._registry[backend_name] = backend_class

    @classmethod
    def get_backend(cls, backend_name: str) -> Callable:
        """Retrieve a backend class by name."""
        if backend_name not in cls._registry:
            raise ValueError(f"Backend '{backend_name}' is not registered.")
        return cls._registry[backend_name]


class OllamaBackend:
    """Wrapper for the Ollama backend."""
    def __init__(self, model_name: str) -> None:
        if Ollama is None:
            raise ImportError("Ollama backend not available.")
        self.llm = Ollama(model=model_name)

    def __call__(self, prompt: str) -> str:
        return self.llm(prompt)


class OpenAIBackend:
    """Wrapper for the OpenAI backend."""
    def __init__(self, model_name: str) -> None:
        if OpenAI is None:
            raise ImportError("OpenAI backend not available.")
        self.llm = OpenAI(model=model_name)

    def __call__(self, prompt: str) -> str:
        return self.llm(prompt)


class HuggingFaceBackend:
    """Wrapper for the HuggingFace backend."""
    def __init__(self, model_name: str) -> None:
        if HuggingFaceHub is None:
            raise ImportError("HuggingFace backend not available.")
        self.llm = HuggingFaceHub(repo_id=model_name)

    def __call__(self, prompt: str) -> str:
        return self.llm(prompt)


def _register_default_backends() -> None:
    """Register default backends for model-agnostic support."""
    ModelRegistry.register('ollama', OllamaBackend)
    ModelRegistry.register('openai', OpenAIBackend)
    ModelRegistry.register('huggingface', HuggingFaceBackend)


_register_default_backends()


class LLM:
    """
    Language Learning Model abstraction supporting multiple backends.
    Handles only model interface and task execution.
    """
    def __init__(self, name: str, model_name: str, backend: str = 'ollama') -> None:
        """
        :param name: The name of the LLM instance.
        :param model_name: The model name for the LLM instance.
        :param backend: The backend to use (e.g., 'ollama', 'openai', 'huggingface').
        :raises ValueError: If any input is invalid.
        """
        if not name or not isinstance(name, str):
            raise ValueError("LLM name must be a non-empty string.")
        if not model_name or not isinstance(model_name, str):
            raise ValueError("model_name must be a non-empty string.")
        if not backend or not isinstance(backend, str):
            raise ValueError("backend must be a non-empty string.")
        self.name: str = name
        self.model_name: str = model_name
        self.backend: str = backend
        self.skill_level: float = random.uniform(50, 100)
        self.evaluations: list = []
        self.llm = ModelRegistry.get_backend(backend)(model_name)

    def perform_task(self, task: str) -> Optional[str]:
        """
        Perform a given task using the LLM.
        :param task: The task to be performed by the LLM.
        :return: The response from the LLM or None if an error occurs.
        """
        if not task or not isinstance(task, str):
            raise ValueError("Task must be a non-empty string.")
        try:
            response = self.llm(task)
            logger.info(f"Response from {self.name}: {response}")
            return response
        except Exception as e:
            logger.exception(f"Error in perform_task for {self.name}: {e}")
            return None


class LLMEvaluationHelper:
    """
    Handles evaluation, score extraction, and skill updating for LLMs.
    """
    @staticmethod
    def evaluate(llm: LLM, original_task: str, task_response: str) -> float:
        if not original_task or not isinstance(original_task, str):
            raise ValueError("original_task must be a non-empty string.")
        if not task_response or not isinstance(task_response, str):
            raise ValueError("task_response must be a non-empty string.")
        try:
            scoring_prompt = (
                f"Task: '{original_task}'. Response: '{task_response}'. "
                "Rate the response numerically between 1 and 9."
            )
            score_response = llm.llm(scoring_prompt)
            logger.info(f"Evaluation by {llm.name}: {score_response}")
            return LLMEvaluationHelper.extract_numerical_score(score_response)
        except Exception as e:
            logger.exception(f"Error in evaluate for {llm.name}: {e}")
            return 0.0

    @staticmethod
    def extract_numerical_score(response_text: str) -> float:
        try:
            matches = re.findall(r'\b(?:[1-9](?:\.\d+)?|10)\b', response_text)
            if matches:
                scores = [float(match) for match in matches]
                average_score = sum(scores) / len(scores)
                return average_score
            return 0.0
        except Exception as e:
            logger.exception(f"Error in extract_numerical_score: {e}")
            return 0.0

    @staticmethod
    def update_skill_level(llm: LLM) -> float:
        try:
            if llm.evaluations:
                new_skill_level = sum(llm.evaluations) / len(llm.evaluations)
                change_in_skill_level = abs(new_skill_level - llm.skill_level)
                llm.skill_level = new_skill_level
                llm.evaluations = []
                return change_in_skill_level
            return 0.0
        except Exception as e:
            logger.exception(
                f"Error in update_skill_level for {llm.name}: {e}")
            return 0.0
