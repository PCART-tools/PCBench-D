def use_autoheuristic(name: str) -> bool:
    return name in torch._inductor.config.autoheuristic_use.split(",")
