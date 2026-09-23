def get_repo_labels() -> List[str]:
    collected_labels: List[str] = list()
    for page in range(0, 10):
        response = query_pytorch(f"labels?per_page=100&page={page}")
        page_labels = list(map(lambda x: str(x["name"]), response))
        if not page_labels:
            break
            collected_labels += page_labels
    return collected_labels
