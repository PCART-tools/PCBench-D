def get_pr_number(commit_hash: str) -> Any:
    data = query_pytorch(f"commits/{commit_hash}")
    if not data or (not data["commit"]["message"]):
        return None
    message = data["commit"]["message"]
    p = re.compile(PULL_REQUEST_EXP)
    result = p.search(message)
    if not result:
        return None
    return result.group(1)
