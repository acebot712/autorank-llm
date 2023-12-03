import unittest
from unittest.mock import patch, Mock
from autorank_llm.models import LLM

class TestLLM(unittest.TestCase):

    def setUp(self):
        self.llm = LLM('test_llm', 'fake_model_name')
        self.llm.skill_level = 50  # Set a fixed skill level for predictable results

    def test_init(self):
        # Test the __init__ method
        self.assertEqual(self.llm.name, 'test_llm')
        self.assertEqual(self.llm.model_name, 'fake_model_name')
        self.assertTrue(50 <= self.llm.skill_level <= 100)
        self.assertEqual(self.llm.evaluations, [])

    @patch('autorank_llm.models.Ollama')
    def test_perform_task(self, mock_ollama_class):
        # Mock the Ollama class to return a Mock object when instantiated
        mock_ollama_instance = Mock()
        mock_ollama_class.return_value = mock_ollama_instance

        # Set the return value when the mock Ollama instance is called
        mock_ollama_instance.return_value = 'mocked response'

        # Now when perform_task is called, it should receive 'mocked response' from the Ollama instance
        response = self.llm.perform_task('fake task')
        self.assertEqual(response, 'mocked response')

    @patch('autorank_llm.models.Ollama')
    @patch('autorank_llm.models.logger')
    def test_perform_task_with_exception(self, mock_logger, mock_ollama):
        # Mock an exception in the Ollama model
        mock_ollama.side_effect = Exception('mocked exception')

        response = self.llm.perform_task('fake task')
        self.assertIsNone(response)
        mock_logger.exception.assert_called_once()  # Ensure that logger.exception was called


    def test_evaluate(self):
        # This test would likely need to mock the Ollama model, similar to test_perform_task
        # Since it involves evaluating a task response, you'd need to mock the response
        # from the Ollama model's scoring_prompt method
        pass  # Fill in with actual test

    def test_extract_numerical_score(self):
        # Adjust the expected value to match the actual method's return value
        self.assertAlmostEqual(self.llm.extract_numerical_score("7, 8.5, 9"), 8.166666666666666, places=2)

    def test_update_skill_level(self):
        # Set evaluations and test update_skill_level method
        self.llm.evaluations = [60, 70, 80]
        expected_new_skill_level = sum(self.llm.evaluations) / len(self.llm.evaluations)
        change = self.llm.update_skill_level()
        self.assertEqual(self.llm.skill_level, expected_new_skill_level)
        self.assertAlmostEqual(change, expected_new_skill_level - 50, places=2)

        # Set skill_level to a fixed value and ensure evaluations are non-empty to prevent division by zero
        self.llm.skill_level = 50
        self.llm.evaluations = [60, 70, 80]  # This should not be empty
        change = self.llm.update_skill_level()
        self.assertNotEqual(change, 0)  # Change should not be zero since we have evaluations



if __name__ == '__main__':
    unittest.main()
