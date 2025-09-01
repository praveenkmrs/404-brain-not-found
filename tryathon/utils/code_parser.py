from logging import config
from repomix import RepoProcessor, RepomixConfig
import os
import shutil

## REPOMIX documentation - https://github.com/AndersonBY/python-repomix
def _repomix_config(codebase_path) -> RepomixConfig:
    config = RepomixConfig()
    
    # Output settings
    output_path = os.getenv("PARSE_OUTPUT_PATH", "output")
    if os.path.exists(output_path):
        shutil.rmtree(output_path)  # Clear the output directory if it exists
    os.makedirs(output_path, exist_ok=True)

    if codebase_path and codebase_path.startswith("https://"):
        repo_name = codebase_path.split("/")[-1].replace(".git", "")
        config.output.file_path = os.path.join(
            output_path, repo_name, "contents.md"
        )
    elif codebase_path:
        repo_name = codebase_path.split("/")[-1]
        config.output.file_path = os.path.join(
            output_path, repo_name, "contents.md"
        )
    else:
        config.output.file_path = os.path.join(
            output_path, "codebase", "contents.md"
        )
    config.output.style = "markdown"
    config.output.show_line_numbers = True
    config.output.remove_empty_lines = True

    # Security settings
    config.security.enable_security_check = True
    config.security.exclude_suspicious_files = True

    # Include/Ignore patterns
    config.include = ["**/src/**/*", "**/tests/**/*"]
    config.ignore.custom_patterns = ["*.log", "*.tmp"]
    config.ignore.use_gitignore = True

    return config

def parse_codebase(codebase_path: str | None):
    if codebase_path:
        if not os.path.isabs(codebase_path):
            codebase_path = os.path.abspath(os.path.join(os.getcwd(), codebase_path))
        print(f"Parsing codebase at: {codebase_path}")
        processor = RepoProcessor(codebase_path, config=_repomix_config(codebase_path))
        result = processor.process()
        return result
    else:
        print("No valid codebase found.")
        return None

def parse_remote_codebase(repo_url: str | None, branch: str = "main"):
    if repo_url:
        print(f"Parsing remote codebase at: {repo_url}")
        base_config = _repomix_config(repo_url)

        # Remote repository configuration   
        base_config.remote.url = repo_url
        base_config.remote.branch = branch

        processor = RepoProcessor(".", config=base_config)
        result = processor.process()
        return result
    else:
        print("No valid remote codebase found.")
        return None
    
