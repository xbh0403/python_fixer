from fastapi import APIRouter, HTTPException
from app.models.schemas import RepositoryRequest, RequirementsResponse
from app.services.github_service import GitHubService
from app.services.ai_service import AIService

router = APIRouter()
github_service = GitHubService()
ai_service = AIService()

@router.post("/analyze", response_model=RequirementsResponse)
async def analyze_repository(request: RepositoryRequest):
    try:
        # Get repository information
        repo_info = await github_service.get_repository_info(
            str(request.url), 
            request.file_path
        )
        
        # Get fixed requirements from AI (now synchronous)
        fixed_requirements = ai_service.fix_requirements(repo_info)
        
        return RequirementsResponse(
            original_requirements=repo_info["requirements"],
            fixed_requirements=fixed_requirements
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))