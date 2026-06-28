import unittest

from src.services.llm_service import LLMService


class TestLLMService(unittest.TestCase):

    def test_connection(self):

        llm = LLMService()

        response = llm.generate_completion(
            system_prompt="You are a helpful assistant.",
            user_prompt="Reply with exactly: Hello World"
        )

        self.assertIn("Hello", response)


if __name__ == "__main__":
    unittest.main()