def find_torchbench_branch(prbody_file: str) -> str:
    branch_name: str = ""
    with open(prbody_file, "r") as pf:
        lines = map(lambda x: x.strip(), pf.read().splitlines())
        magic_lines = list(filter(lambda x: x.startswith(MAGIC_TORCHBENCH_PREFIX), lines))
        if magic_lines:
            # Only the first magic line will be recognized.
            branch_name = magic_lines[0][len(MAGIC_TORCHBENCH_PREFIX):].strip()
    # If not specified, use main as the default branch
    if not branch_name:
        branch_name = "main"
    return branch_name
