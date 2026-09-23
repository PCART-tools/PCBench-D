async def get_all_files(paths: List[str]) -> List[str]:
    """Returns all files that are tracked by git in the given paths."""
    output = await run_shell_command(["git", "ls-files"] + paths)
    return str(output).strip().splitlines()
