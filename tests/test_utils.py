import unittest
from unittest.mock import Mock
from autorank_llm.utils import normalize_skill_levels, rank_llms

class TestUtils(unittest.TestCase):

    def setUp(self):
        # Setup Mock LLMs with different skill levels
        self.llm1 = Mock(skill_level=80, name='LLM1')
        self.llm2 = Mock(skill_level=70, name='LLM2')
        self.llm3 = Mock(skill_level=90, name='LLM3')
        self.llms = [self.llm1, self.llm2, self.llm3]

    def test_normalize_skill_levels_non_empty_list(self):
        # Test normalization with a non-empty list of LLMs
        normalize_skill_levels(self.llms)
        self.assertEqual(self.llm1.skill_level, 50.0)
        self.assertEqual(self.llm2.skill_level, 0.0)
        self.assertEqual(self.llm3.skill_level, 100.0)

    def test_normalize_skill_levels_empty_list(self):
        # Test normalization with an empty list of LLMs
        with self.assertRaises(ValueError):
            normalize_skill_levels([])

    def test_rank_llms_non_empty_list(self):
        # Test ranking with a non-empty list of LLMs
        ranked_llms = rank_llms(self.llms)
        self.assertEqual(ranked_llms, [self.llm3, self.llm1, self.llm2])

    def test_rank_llms_empty_list(self):
        # Test ranking with an empty list of LLMs
        with self.assertRaises(ValueError):
            rank_llms([])

    def test_rank_llms_return_value(self):
        # Test the return value of rank_llms function
        self.llm1.skill_level = 30
        self.llm2.skill_level = 60
        self.llm3.skill_level = 90
        expected_ranking = [self.llm3, self.llm2, self.llm1]
        self.assertEqual(rank_llms(self.llms), expected_ranking)

    def tearDown(self):
        # Clean up after each test method
        pass

if __name__ == '__main__':
    unittest.main()
