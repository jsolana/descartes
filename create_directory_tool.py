import os

from crewai_tools import BaseTool


class CreateDirectoryTool(BaseTool):
    """
    Custom tool to create directories.

    Attributes:
        path (str): The directory to be created if not exists.
    """
    name: str = "Create Directory Tool"
    description: str = "Create a directory."

    def _run(self, path: str) -> str:
        if not os.path.exists(path):
            os.mkdir(path)
        return f"Created {path}"
