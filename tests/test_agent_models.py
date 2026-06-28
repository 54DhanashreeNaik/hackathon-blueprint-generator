import unittest
from pydantic import ValidationError
from src.models.agent_models import ProblemAnalysisResult

class TestAgentModels(unittest.TestCase):
    """
    Unit tests for validating the ProblemAnalysisResult model structure,
    serialization, deserialization, and field validation constraints.
    """

    def setUp(self):
        self.valid_data = {
            "extracted_problems": ["Problem A", "Problem B"],
            "technical_constraints": ["Constraint A"],
            "target_audiences": ["Audience A"],
            "assumptions": ["Assumption A"],
            "risks": ["Risk A"],
            "raw_output": "This is raw output text from Gemini."
        }

    def test_valid_model_creation(self):
        """
        Verifies that a valid ProblemAnalysisResult model is successfully instantiated
        and all fields are correctly initialized.
        """
        model = ProblemAnalysisResult(**self.valid_data)
        
        self.assertEqual(model.extracted_problems, ["Problem A", "Problem B"])
        self.assertEqual(model.technical_constraints, ["Constraint A"])
        self.assertEqual(model.target_audiences, ["Audience A"])
        self.assertEqual(model.assumptions, ["Assumption A"])
        self.assertEqual(model.risks, ["Risk A"])
        self.assertEqual(model.raw_output, "This is raw output text from Gemini.")

    def test_model_dump(self):
        """
        Verifies that model_dump correctly serializes the model to a dictionary.
        """
        model = ProblemAnalysisResult(**self.valid_data)
        dumped_dict = model.model_dump()
        
        self.assertIsInstance(dumped_dict, dict)
        self.assertEqual(dumped_dict["extracted_problems"], ["Problem A", "Problem B"])
        self.assertEqual(dumped_dict["raw_output"], "This is raw output text from Gemini.")

    def test_model_dump_json(self):
        """
        Verifies that model_dump_json correctly serializes the model to a JSON string.
        """
        model = ProblemAnalysisResult(**self.valid_data)
        json_str = model.model_dump_json()
        
        self.assertIsInstance(json_str, str)
        self.assertIn('"extracted_problems":["Problem A","Problem B"]', json_str)
        self.assertIn('"raw_output":"This is raw output text from Gemini."', json_str)

    def test_validation_missing_required_fields(self):
        """
        Verifies that Pydantic raises ValidationError when required fields (like raw_output) are missing.
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["raw_output"]
        
        with self.assertRaises(ValidationError) as context:
            ProblemAnalysisResult(**invalid_data)
            
        self.assertIn("raw_output", str(context.exception))

    def test_default_factories(self):
        """
        Verifies that lists default to empty lists if they are omitted.
        """
        minimal_data = {"raw_output": "Minimal raw text."}
        model = ProblemAnalysisResult(**minimal_data)
        
        self.assertEqual(model.extracted_problems, [])
        self.assertEqual(model.technical_constraints, [])
        self.assertEqual(model.target_audiences, [])
        self.assertEqual(model.assumptions, [])
        self.assertEqual(model.risks, [])
        self.assertEqual(model.raw_output, "Minimal raw text.")

if __name__ == "__main__":
    unittest.main()
