from pydantic import BaseModel, HttpUrl

class RepositoryRequest(BaseModel):
    url: HttpUrl
    file_path: str = "requirements.txt"  # default to requirements.txt

class RequirementsResponse(BaseModel):
    original_requirements: str
    fixed_requirements: str
    error_message: str | None = None