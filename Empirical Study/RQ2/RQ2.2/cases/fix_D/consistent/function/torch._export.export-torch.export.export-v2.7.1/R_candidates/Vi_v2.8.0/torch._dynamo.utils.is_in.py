def is_in(item: Any, *containers) -> bool:
    for container in containers:
        if item in container:
            return True
    return False
