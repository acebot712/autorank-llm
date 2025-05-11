import unittest
from unittest.mock import patch, Mock
from autorank_llm.models import LLM, ModelRegistry

class TestLLM(unittest.TestCase):

    def setUp(self):
        self.llm = LLM('test_llm', 'fake_model_name', backend='ollama')
        self.llm.skill_level = 50  # Set a fixed skill level for predictable results

    def test_init(self):
        # Test the __init__ method
        self.assertEqual(self.llm.name, 'test_llm')
        self.assertEqual(self.llm.model_name, 'fake_model_name')
        self.assertTrue(50 <= self.llm.skill_level <= 100)
        self.assertEqual(self.llm.evaluations, [])
        self.assertEqual(self.llm.backend, 'ollama')

    @patch('autorank_llm.models.OllamaBackend')
    def test_perform_task(self, mock_backend_class):
        # Mock the backend class to return a Mock object when instantiated
        mock_backend_instance = Mock()
        mock_backend_class.return_value = mock_backend_instance
        mock_backend_instance.__call__.return_value = 'mocked response'
        llm = LLM('test_llm', 'fake_model_name', backend='ollama')
        llm.llm = mock_backend_instance
        response = llm.perform_task('fake task')
        self.assertEqual(response, 'mocked response')

    @patch('autorank_llm.models.OllamaBackend')
    @patch('autorank_llm.models.logger')
    def test_perform_task_with_exception(self, mock_logger, mock_backend_class):
        # Mock an exception in the backend
        mock_backend_instance = Mock()
        mock_backend_instance.__call__.side_effect = Exception('mocked exception')
        mock_backend_class.return_value = mock_backend_instance
        llm = LLM('test_llm', 'fake_model_name', backend='ollama')
        llm.llm = mock_backend_instance
        response = llm.perform_task('fake task')
        self.assertIsNone(response)
        mock_logger.exception.assert_called_once()  # Ensure that logger.exception was called

    def test_extract_numerical_score(self):
        self.assertAlmostEqual(self.llm.extract_numerical_score("7, 8.5, 9"), 8.166666666666666, places=2)

    def test_update_skill_level(self):
        self.llm.evaluations = [60, 70, 80]
        expected_new_skill_level = sum(self.llm.evaluations) / len(self.llm.evaluations)
        change = self.llm.update_skill_level()
        self.assertEqual(self.llm.skill_level, expected_new_skill_level)
        self.assertAlmostEqual(change, expected_new_skill_level - 50, places=2)
        self.llm.skill_level = 50
        self.llm.evaluations = [60, 70, 80]
        change = self.llm.update_skill_level()
        self.assertNotEqual(change, 0)

    def test_model_registry(self):
        # Test backend registration and retrieval
        class DummyBackend:
            def __init__(self, model_name):
                self.model_name = model_name
            def __call__(self, prompt):
                return f"Dummy: {prompt}"
        ModelRegistry.register('dummy', DummyBackend)
        backend = ModelRegistry.get_backend('dummy')
        self.assertEqual(backend, DummyBackend)
        instance = backend('foo')
        self.assertEqual(instance('bar'), "Dummy: bar")
        # Test error on unknown backend
        with self.assertRaises(ValueError):
            ModelRegistry.get_backend('not_a_backend')

if __name__ == '__main__':
    unittest.main()
