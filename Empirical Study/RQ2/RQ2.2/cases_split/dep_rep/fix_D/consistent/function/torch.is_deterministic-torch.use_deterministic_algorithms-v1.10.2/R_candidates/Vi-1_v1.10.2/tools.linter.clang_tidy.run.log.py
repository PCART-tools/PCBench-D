def log(*args: Any, **kwargs: Any) -> None:
    if not QUIET:
        print(*args, **kwargs)
