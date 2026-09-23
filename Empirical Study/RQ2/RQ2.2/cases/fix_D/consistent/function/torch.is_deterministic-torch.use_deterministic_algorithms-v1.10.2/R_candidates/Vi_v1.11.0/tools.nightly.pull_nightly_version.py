@timed("Pulling nightly PyTorch")
def pull_nightly_version(spdir: str) -> None:
    """Fetches the nightly version and then merges it ."""
    nightly_version = _nightly_version(spdir)
    cmd = ["git", "merge", nightly_version]
    p = subprocess.run(cmd, check=True)
