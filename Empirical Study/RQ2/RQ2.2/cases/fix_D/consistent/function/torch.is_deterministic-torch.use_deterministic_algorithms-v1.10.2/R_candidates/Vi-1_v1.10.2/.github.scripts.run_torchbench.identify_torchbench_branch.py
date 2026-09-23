def identify_torchbench_branch(torchbench_path: str, prbody_file: str) -> None:
    branch_name: str
    with open(prbody_file, "r") as pf:
        lines = map(lambda x: x.strip(), pf.read().splitlines())
        magic_lines = list(filter(lambda x: x.startswith(MAGIC_TORCHBENCH_PREFIX), lines))
        if magic_lines:
            # Only the first magic line will be recognized.
            branch_name = magic_lines[0][len(MAGIC_TORCHBENCH_PREFIX):].strip()
    # If not specified, directly return without the branch checkout
    if not branch_name:
        return
    try:
        print(f"Checking out the TorchBench branch: {branch_name} ...")
        repo = git.Repo(torchbench_path)
        origin = repo.remotes.origin
        origin.fetch(branch_name)
        repo.create_head(branch_name, origin.refs[branch_name]).checkout()
    except git.exc.GitCommandError:
        raise RuntimeError(f'{branch_name} doesn\'t exist in the pytorch/benchmark repository. Please double check.')
