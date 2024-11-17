import pytest
import sys
sys.path.append("/Users/xbh0403/Desktop/websites/backend")
from app.services.github_service import GitHubService
from app.services.ai_service import AIService
import os
from dotenv import load_dotenv

# Load environment variables before tests
load_dotenv()

@pytest.mark.asyncio
async def test_github_service():
    service = GitHubService()
    # Test with a public repository
    repo_url = "https://github.com/evo-design/evo"
    
    result = await service.get_repository_info(repo_url)
    
    assert "requirements" in result
    assert "initial_date" in result
    assert "imports" in result
    assert isinstance(result["imports"], list)

@pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="ANTHROPIC_API_KEY not set")
def test_ai_service():  # Removed async
    service = AIService()
    
    mock_repo_info = {
        "requirements": "pandas\nnumpy\nscikit-learn",
        "initial_date": "2024-01-01",
        "imports": ["import pandas as pd", "import numpy as np"]
    }
    
    result = service.fix_requirements(mock_repo_info)
    assert isinstance(result, str)
    assert len(result) > 0
    assert any(pkg in result.lower() for pkg in ['pandas', 'numpy', 'scikit-learn'])


if __name__ == "__main__":
    pytest.main([__file__])