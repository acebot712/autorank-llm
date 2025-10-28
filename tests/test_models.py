import unittest
from unittest.mock import patch, Mock
from autorank_llm.models import (
    LLM,
    ModelRegistry,
    LLMEvaluationHelper
)


class TestModelRegistry(unittest.TestCase):
    """Test the ModelRegistry system."""

    def test_register_and_get_backend(self):
        """Test backend registration and retrieval."""
        class DummyBackend:
            def __init__(self, model_name):
                self.model_name = model_name

            def __call__(self, prompt):
                return f"Dummy: {prompt}"

        ModelRegistry.register('dummy_test', DummyBackend)
        backend = ModelRegistry.get_backend('dummy_test')
        self.assertEqual(backend, DummyBackend)
        instance = backend('test_model')
        self.assertEqual(instance('hello'), "Dummy: hello")

    def test_get_unknown_backend_raises_error(self):
        """Test that getting an unknown backend raises ValueError."""
        with self.assertRaises(ValueError) as context:
            ModelRegistry.get_backend('definitely_not_a_backend')
        self.assertIn('not registered', str(context.exception))


class TestLLM(unittest.TestCase):
    """Test the LLM class."""

    def setUp(self):
        """Set up test fixtures with mocked backend."""
        # Mock a test backend
        class MockBackend:
            def __init__(self, model_name):
                self.model_name = model_name

            def __call__(self, prompt):
                return f"Response to: {prompt}"

        ModelRegistry.register('mock', MockBackend)
        self.llm = LLM('test_llm', 'test_model', backend='mock')
        self.llm.skill_level = 50.0

    def test_init(self):
        """Test LLM initialization."""
        llm = LLM('my_llm', 'my_model', backend='mock')
        self.assertEqual(llm.name, 'my_llm')
        self.assertEqual(llm.model_name, 'my_model')
        self.assertEqual(llm.backend, 'mock')
        self.assertTrue(50 <= llm.skill_level <= 100)
        self.assertEqual(llm.evaluations, [])

    def test_init_validation(self):
        """Test that LLM validates inputs."""
        with self.assertRaises(ValueError):
            LLM('', 'model', backend='mock')
        with self.assertRaises(ValueError):
            LLM('name', '', backend='mock')
        with self.assertRaises(ValueError):
            LLM('name', 'model', backend='')

    def test_perform_task(self):
        """Test performing a task."""
        response = self.llm.perform_task('test task')
        self.assertEqual(response, 'Response to: test task')

    def test_perform_task_validation(self):
        """Test that perform_task validates inputs."""
        with self.assertRaises(ValueError):
            self.llm.perform_task('')
        with self.assertRaises(ValueError):
            self.llm.perform_task(None)

    @patch('autorank_llm.models.logger')
    def test_perform_task_handles_exceptions(self, mock_logger):
        """Test that perform_task handles exceptions gracefully."""
        self.llm.llm = Mock(side_effect=Exception('test error'))
        response = self.llm.perform_task('test task')
        self.assertIsNone(response)
        mock_logger.exception.assert_called_once()


class TestLLMEvaluationHelper(unittest.TestCase):
    """Test the LLMEvaluationHelper class."""

    def setUp(self):
        """Set up test fixtures."""
        class MockBackend:
            def __init__(self, model_name):
                self.model_name = model_name

            def __call__(self, prompt):
                return "The score is 8 out of 10"

        ModelRegistry.register('mock_eval', MockBackend)
        self.llm = LLM('evaluator', 'model', backend='mock_eval')

    def test_extract_numerical_score_single(self):
        """Test extracting a single numerical score."""
        score = LLMEvaluationHelper.extract_numerical_score("The score is 7")
        self.assertEqual(score, 7.0)

    def test_extract_numerical_score_multiple(self):
        """Test extracting multiple scores and averaging."""
        score = LLMEvaluationHelper.extract_numerical_score(
            "Scores are 7, 8, and 9"
        )
        self.assertAlmostEqual(score, 8.0, places=2)

    def test_extract_numerical_score_with_decimals(self):
        """Test extracting decimal scores."""
        score = LLMEvaluationHelper.extract_numerical_score(
            "7.5, 8.5, 9.0"
        )
        self.assertAlmostEqual(score, 8.333333, places=2)

    def test_extract_numerical_score_no_match(self):
        """Test that no matches returns 0."""
        score = LLMEvaluationHelper.extract_numerical_score(
            "No numbers here"
        )
        self.assertEqual(score, 0.0)

    def test_evaluate(self):
        """Test the evaluate method."""
        score = LLMEvaluationHelper.evaluate(
            self.llm,
            "Test task",
            "Test response"
        )
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)

    def test_evaluate_validation(self):
        """Test that evaluate validates inputs."""
        with self.assertRaises(ValueError):
            LLMEvaluationHelper.evaluate(self.llm, '', 'response')
        with self.assertRaises(ValueError):
            LLMEvaluationHelper.evaluate(self.llm, 'task', '')

    def test_update_skill_level(self):
        """Test updating skill level based on evaluations."""
        self.llm.skill_level = 50.0
        self.llm.evaluations = [60.0, 70.0, 80.0]

        change = LLMEvaluationHelper.update_skill_level(self.llm)

        expected_skill = 70.0  # average of [60, 70, 80]
        self.assertEqual(self.llm.skill_level, expected_skill)
        self.assertAlmostEqual(change, 20.0, places=2)
        self.assertEqual(self.llm.evaluations, [])  # Should be cleared

    def test_update_skill_level_no_evaluations(self):
        """Test that update_skill_level handles empty evaluations."""
        self.llm.skill_level = 50.0
        self.llm.evaluations = []

        change = LLMEvaluationHelper.update_skill_level(self.llm)

        self.assertEqual(change, 0.0)
        self.assertEqual(self.llm.skill_level, 50.0)


if __name__ == '__main__':
    unittest.main()
