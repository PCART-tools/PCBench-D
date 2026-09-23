def check_branch(subcommand: str, branch: Optional[str]) -> Optional[str]:
    """Checks that the branch name can be checked out."""
    if subcommand != "checkout":
        return None
    # first make sure actual branch name was given
    if branch is None:
        return "Branch name to checkout must be supplied with '-b' option"
    # next check that the local repo is clean
    cmd = ["git", "status", "--untracked-files=no", "--porcelain"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, universal_newlines=True)
    if p.stdout.strip():
        return "Need to have clean working tree to checkout!\n\n" + p.stdout
    # next check that the branch name doesn't already exist
    cmd = ["git", "show-ref", "--verify", "--quiet", "refs/heads/" + branch]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)  # type: ignore[assignment]
    if not p.returncode:
        return f"Branch {branch!r} already exists"
    return None
