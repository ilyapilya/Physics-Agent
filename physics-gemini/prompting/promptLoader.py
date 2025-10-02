import yaml
from typing import Tuple
from pathlib import Path

class PromptLoader:
    
    def __init__(self):
        self.prompt_path = Path(__file__).parent / "prompts.yaml"

    # Load and return string wrapper of markup file
    def load_prompt(self, prompt_name: str = "core_physics_prompt") -> str:
        try:
            with open(self.prompt_path, 'r') as file:
                prompts = yaml.safe_load(file)

            if 'prompts' not in prompts or prompt_name not in prompts['prompts']:
                raise ValueError(f"Prompt {prompt_name} not in markup file")
            
            prompt_data = prompts['prompts'][prompt_name]
            
            formatted_prompt = (
                f"Description: {prompt_data['description']}\n"
                f"Hypothesis: {prompt_data['hypothesis']}\n"
                f"Question: {prompt_data['question']}"
            )

            return formatted_prompt
        except Exception as e:
            if isinstance(e, FileNotFoundError):
                raise FileNotFoundError(f"Prompt file not found at {self.prompt_path}")
            raise ValueError(f"Error loading prompt: {str(e)}")