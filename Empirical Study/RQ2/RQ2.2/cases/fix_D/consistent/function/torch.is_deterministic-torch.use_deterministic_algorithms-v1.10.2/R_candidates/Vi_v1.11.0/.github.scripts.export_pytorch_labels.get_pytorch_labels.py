@lru_cache()
def get_pytorch_labels() -> List[str]:
    prefix = "https://api.github.com/repos/pytorch/pytorch/labels?per_page=100"
    header, info = request_for_labels(prefix + "&page=1")
    labels: List[str] = []
    update_labels(labels, info)

    last_page = get_last_page(header)
    assert last_page > 0, "Error reading header info to determine total number of pages of labels"
    for page_number in range(2, last_page + 1):  # skip page 1
        _, info = request_for_labels(prefix + f"&page={page_number}")
        update_labels(labels, info)

    return labels
