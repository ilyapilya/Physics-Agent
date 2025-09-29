import unittest
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Add the parent directory to Python path to import from physics-langchain
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "physics-langchain"))
from routes.api import parseApiKey

class TestGeminiAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment before any tests run"""
        load_dotenv()
        cls.api_key = None
        try:
            cls.api_key = parseApiKey()
            genai.configure(api_key=cls.api_key)
            cls.model = genai.GenerativeModel("gemini-pro")
        except Exception as e:
            print(f"Setup failed: {str(e)}")
            cls.model = None

    def test_api_key_parsing(self):
        """Test if API key is properly parsed from environment variables"""
        self.assertIsNotNone(self.api_key, "API key should not be None")
        self.assertIsInstance(self.api_key, str, "API key should be a string")
        self.assertTrue(len(self.api_key) > 0, "API key should not be empty")

    def test_gemini_model_initialization(self):
        """Test if Gemini model is properly initialized"""
        self.assertIsNotNone(self.model, "Gemini model should be initialized")

    def test_gemini_basic_response(self):
        """Test if Gemini model can generate a basic response"""
        if not self.model:
            self.skipTest("Model not initialized, skipping test")
        
        prompt = "What is the theory of relativity?"
        try:
            response = self.model.generate_content(prompt)
            self.assertIsNotNone(response, "Response should not be None")
            self.assertTrue(len(response.text) > 0, "Response should not be empty")
            print(f"\nTest response from Gemini:\n{response.text[:200]}...")
        except Exception as e:
            self.fail(f"Failed to get response from Gemini: {str(e)}")

    def test_gemini_chat_functionality(self):
        """Test if Gemini model can maintain a chat conversation"""
        if not self.model:
            self.skipTest("Model not initialized, skipping test")
        
        try:
            chat = self.model.start_chat()
            
            # Test multiple message exchanges
            responses = []
            messages = [
                "Hello, I'd like to learn about physics.",
                "Can you explain Newton's laws of motion?",
                "What about conservation of energy?"
            ]
            
            for message in messages:
                response = chat.send_message(message)
                responses.append(response.text)
                self.assertIsNotNone(response, f"Response should not be None for message: {message}")
                self.assertTrue(len(response.text) > 0, f"Response should not be empty for message: {message}")
            
            print("\nTest chat responses from Gemini:")
            for i, response in enumerate(responses, 1):
                print(f"\nMessage {i} response preview:\n{response[:100]}...")
                
        except Exception as e:
            self.fail(f"Failed to test chat functionality: {str(e)}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
