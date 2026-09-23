def get_base_commit(sha1: str) -> str:
    return subprocess.check_output(
        ["git", "merge-base", sha1, "origin/release/1.10"],
        encoding="ascii",
    ).strip()
