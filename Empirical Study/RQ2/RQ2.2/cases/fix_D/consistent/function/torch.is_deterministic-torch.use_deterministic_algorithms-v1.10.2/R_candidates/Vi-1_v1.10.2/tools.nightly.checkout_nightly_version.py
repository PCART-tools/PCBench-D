@timed("Checking out nightly PyTorch")
def checkout_nightly_version(branch: str, spdir: str) -> None:
    """Get's the nightly version and then checks it out."""
    nightly_version = _nightly_version(spdir)
    cmd = ["git", "checkout", "-b", branch, nightly_version]
    p = subprocess.run(cmd, check=True)
