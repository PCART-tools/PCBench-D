def get_pr_author_and_labels(pr_number: int) -> Tuple[str, Set[str]]:
    # See https://docs.github.com/en/rest/reference/pulls#get-a-pull-request
    data = query_pytorch(f"pulls/{pr_number}")
    user = data["user"]["login"]
    labels = {label["name"] for label in data["labels"]}
    return user, labels
