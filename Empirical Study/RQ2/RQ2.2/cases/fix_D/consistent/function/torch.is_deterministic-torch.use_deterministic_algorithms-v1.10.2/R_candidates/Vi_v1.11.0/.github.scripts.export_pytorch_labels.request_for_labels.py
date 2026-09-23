def request_for_labels(url: str) -> Any:
    headers = {'Accept': 'application/vnd.github.v3+json'}
    return _read_url(Request(url, headers=headers))
