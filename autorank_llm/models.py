import re
import random
from langchain.llms import Ollama
import logging

# Set up a specific logger for this module
logger = logging.getLogger(__name__)

class LLM:
    def __init__(self, name, model_name):
        """
        Initialize an instance of LLM with a given name and model.

        :param name: The name of the LLM instance.
        :param model_name: The model name for the LLM instance.
        """
        self.name = name
        self.model_name = model_name
        self.skill_level = random.uniform(50, 100)
        self.evaluations = []

    def perform_task(self, task):
        """
        Perform a given task using the LLM.

        :param task: The task to be performed by the LLM.
        :return: The response from the LLM or None if an error occurs.
        """
        try:
            llm = Ollama(model=self.model_name)
            response = llm(task)
            logger.info(f"Response from {self.name}: {response}")
            return response
        except Exception as e:
            logger.exception(f"Error in perform_task for {self.name}: {e}")
            return None

    def evaluate(self, original_task, task_response):
        """
        Evaluate a response given by an LLM based on the original task.

        :param original_task: The original task given to the LLM.
        :param task_response: The response provided by the LLM.
        :return: The numerical score of the response.
        """
        try:
            scoring_prompt = f"Task: '{original_task}'. Response: '{task_response}'. Rate the response numerically between 1 and 9."
            llm = Ollama(model=self.model_name)
            score_response = llm(scoring_prompt)
            logger.info(f"Evaluation by {self.name}: {score_response}")
            return self.extract_numerical_score(score_response)
        except Exception as e:
            logger.exception(f"Error in evaluate for {self.name}: {e}")
            return 0

    def extract_numerical_score(self, response_text):
        """
        Extract a numerical score from the text response.

        :param response_text: The text response containing the numerical score.
        :return: The extracted numerical score as a float or 0 if no score is found.
        """
        try:
            matches = re.findall(r'\b(?:[1-9](?:\.\d+)?|10)\b', response_text)
            if matches:
                scores = [float(match) for match in matches]
                average_score = sum(scores) / len(scores)
                return average_score
            else:
                return 0
        except Exception as e:
            logger.exception(f"Error in extract_numerical_score: {e}")
            return 0

    def update_skill_level(self):
        """
        Update the skill level of the LLM based on the evaluations received.

        :return: The change in skill level as a float.
        """
        try:
            if self.evaluations:
                new_skill_level = sum(self.evaluations) / len(self.evaluations)
                change_in_skill_level = abs(new_skill_level - self.skill_level)
                self.skill_level = new_skill_level
                self.evaluations = []
                return change_in_skill_level
            return 0
        except Exception as e:
            logger.exception(f"Error in update_skill_level for {self.name}: {e}")
            return 0
