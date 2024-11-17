import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIService:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = Anthropic(api_key=api_key)

    def fix_requirements(self, repo_info: dict) -> str:
        try:
            error_message = repo_info.get('error_message', '')
            error_prompt = f"\n4. Error message reported:\n{error_message}" if error_message else ""
            
            prompt = (
                "Given a Python project with the following information:\n"
                "1. Original requirements.txt:\n"
                f"{repo_info['requirements']}\n\n"
                f"2. Project start date: {repo_info['initial_date']}\n\n"
                "3. Imports used in the project:\n"
                f"{chr(10).join(repo_info['imports'])}\n"
                f"{error_prompt}\n\n"
                "Please analyze this information and provide an updated requirements.txt with appropriate version numbers.\n"
                "Consider:\n"
                "- Compatibility between packages\n"
                "- Project start date for version selection\n"
                "- Actually used imports\n"
                "- Security updates\n"
                "- Any error messages provided\n\n"
                "Return only the updated requirements.txt content without any explanation."
            )

            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0,
                system="You are a Python dependency expert. Provide only the updated requirements.txt content.",
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text
        
        except Exception as e:
            print(f"Error in AI Service: {str(e)}")
            raise