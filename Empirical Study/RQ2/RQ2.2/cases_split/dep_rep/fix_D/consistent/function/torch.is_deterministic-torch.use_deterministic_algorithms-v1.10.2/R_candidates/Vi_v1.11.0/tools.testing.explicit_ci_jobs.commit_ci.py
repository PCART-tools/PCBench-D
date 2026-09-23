def commit_ci(files: List[str], message: str) -> None:
    # Check that there are no other modified files than the ones edited by this
    # tool
    stdout = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE).stdout.decode()
    for line in stdout.split("\n"):
        if line == "":
            continue
        if line[0] != " ":
            raise RuntimeError(f"Refusing to commit while other changes are already staged: {line}")


    # Make the commit
    subprocess.run(["git", "add"] + files)
    subprocess.run(["git", "commit", "-m", message])
