def bind(optional: Optional[_T], fn: Callable[[_T], _R]) -> Optional[_R]:
    if optional is None:
        return None
    return fn(optional)
