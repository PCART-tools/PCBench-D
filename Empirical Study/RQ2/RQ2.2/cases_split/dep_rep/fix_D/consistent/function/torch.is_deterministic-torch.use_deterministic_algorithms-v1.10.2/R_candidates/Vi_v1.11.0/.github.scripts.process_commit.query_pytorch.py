def query_pytorch(cmd: str) -> Any:
    response = requests.get(f"{PYTORCH_REPO}/{cmd}", headers=REQUEST_HEADERS)
    return response.json()
