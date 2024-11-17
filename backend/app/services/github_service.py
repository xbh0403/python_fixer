import os
from git import Repo
import tempfile
from datetime import datetime

class GitHubService:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()

    async def get_repository_info(self, repo_url: str, file_path: str = "requirements.txt", error_message: str | None = None):
        try:
            # Clone the repository
            repo = Repo.clone_from(repo_url, self.temp_dir)
            
            # Get file content
            file_path = os.path.join(self.temp_dir, file_path)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Cannot find {file_path}")
            
            with open(file_path, 'r') as f:
                requirements_content = f.read()

            # Get initial commit date
            initial_commit = list(repo.iter_commits())[-1]
            initial_date = datetime.fromtimestamp(initial_commit.committed_date)

            # Get all Python files
            python_files = []
            for root, _, files in os.walk(self.temp_dir):
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))

            # Extract imports from Python files
            imports = set()
            for py_file in python_files:
                with open(py_file, 'r', encoding='utf-8') as f:
                    try:
                        content = f.read()
                        # Basic import extraction (can be improved)
                        for line in content.split('\n'):
                            if line.strip().startswith('import ') or line.strip().startswith('from '):
                                imports.add(line.strip())
                    except UnicodeDecodeError:
                        continue

            return {
                "requirements": requirements_content,
                "initial_date": initial_date.isoformat(),
                "imports": list(imports),
                "files": python_files,
                "error_message": error_message
            }

        finally:
            # Cleanup
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)