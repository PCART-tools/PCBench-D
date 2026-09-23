def get_git_remote_name() -> str:
    return os.getenv("GIT_REMOTE_NAME", "origin")
