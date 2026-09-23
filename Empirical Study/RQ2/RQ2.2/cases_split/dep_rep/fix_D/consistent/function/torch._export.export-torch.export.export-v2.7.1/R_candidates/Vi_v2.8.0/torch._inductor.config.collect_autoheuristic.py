def collect_autoheuristic(name: str) -> bool:
    return name in torch._inductor.config.autoheuristic_collect.split(",")
