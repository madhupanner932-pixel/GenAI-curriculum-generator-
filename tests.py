import unittest
import streamlit as st
from utils.llm import query_model
from utils.prompts import generate_prompt
from utils.storage import save_data, load_data
from utils.assessment import get_assessment
from utils.visualizations import create_chart
from utils.reports import generate_report

class TestApp(unittest.TestCase):
    def test_llm_query(self):
        prompt = get_chat_prompt("AI", "career guidance", "What is AI?")
        response = query_model(prompt)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_storage(self):
        test_data = {"name": "Test User", "score": 90}
        save_data("test", test_data)
        loaded = load_data("test")
        self.assertEqual(test_data, loaded)

    def test_assessment(self):
        result = get_assessment(["Python", "AI"])
        self.assertIn("score", result)

    def test_visualization(self):
        chart = create_chart([1, 2, 3], [4, 5, 6])
        self.assertIsNotNone(chart)

    def test_report(self):
        report = generate_report({"name": "Test", "score": 80})
        self.assertIsInstance(report, str)

if __name__ == "__main__":
    unittest.main()
