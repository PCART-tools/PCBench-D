def run_autoheuristic(name: str) -> bool:
    return collect_autoheuristic(name) or use_autoheuristic(name)
