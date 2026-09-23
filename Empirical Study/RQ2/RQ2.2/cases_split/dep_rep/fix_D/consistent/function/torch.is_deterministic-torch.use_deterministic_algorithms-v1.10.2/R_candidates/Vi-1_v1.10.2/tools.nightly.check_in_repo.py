def check_in_repo() -> Optional[str]:
    """Ensures that we are in the PyTorch repo."""
    if not os.path.isfile("setup.py"):
        return "Not in root-level PyTorch repo, no setup.py found"
    with open("setup.py") as f:
        s = f.read()
    if "PyTorch" not in s:
        return "Not in PyTorch repo, 'PyTorch' not found in setup.py"
    return None
