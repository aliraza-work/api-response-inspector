import unittest
from src.inspector import inspect_payload

class InspectorTests(unittest.TestCase):
    def test_missing_and_empty(self):
        result = inspect_payload({"id": "1", "title": ""}, ["id", "title", "status"])
        self.assertFalse(result["ok"])
        self.assertIn("status", result["missing_fields"])
        self.assertIn("title", result["empty_fields"])

if __name__ == "__main__":
    unittest.main()
