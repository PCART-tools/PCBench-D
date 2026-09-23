def find_current_branch(repo_path: str) -> str:
    repo = git.Repo(repo_path)
    name: str = repo.active_branch.name
    return name
