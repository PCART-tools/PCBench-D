def _ensure_commit(git_sha1: str) -> None:
    """Make sure that we actually have the commit locally"""
    cmd = ["git", "cat-file", "-e", git_sha1 + "^{commit}"]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if p.returncode == 0:
        # we have the commit locally
        return
    # we don't have the commit, must fetch
    cmd = ["git", "fetch", "https://github.com/pytorch/pytorch.git", git_sha1]
    p = subprocess.run(cmd, check=True)
