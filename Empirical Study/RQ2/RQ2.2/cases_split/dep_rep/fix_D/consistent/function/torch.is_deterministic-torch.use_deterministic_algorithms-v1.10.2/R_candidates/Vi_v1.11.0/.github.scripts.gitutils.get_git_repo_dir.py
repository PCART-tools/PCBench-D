def get_git_repo_dir() -> str:
    from pathlib import Path
    return os.getenv("GIT_REPO_DIR", str(Path(__file__).resolve().parent.parent.parent))
