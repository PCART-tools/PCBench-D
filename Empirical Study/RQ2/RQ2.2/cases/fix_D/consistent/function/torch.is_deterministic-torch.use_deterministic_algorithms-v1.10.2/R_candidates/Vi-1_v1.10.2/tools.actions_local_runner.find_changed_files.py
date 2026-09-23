def find_changed_files() -> List[str]:
    untracked = []

    for line in git(["status", "--porcelain"]):
        # Untracked files start with ??, so grab all of those
        if line.startswith("?? "):
            untracked.append(line.replace("?? ", ""))

    # Modified, unstaged
    modified = git(["diff", "--name-only"])

    # Modified, staged
    cached = git(["diff", "--cached", "--name-only"])

    # Committed
    merge_base = git(["merge-base", "origin/master", "HEAD"])[0]
    diff_with_origin = git(["diff", "--name-only", merge_base, "HEAD"])

    # De-duplicate
    all_files = set()
    for x in untracked + cached + modified + diff_with_origin:
        stripped = x.strip()
        if stripped != "" and os.path.exists(stripped):
            all_files.add(stripped)
    return list(all_files)
