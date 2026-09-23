def _check_for_pydantic(obj: Any) -> bool:
    return _PYDANTIC_AVAILABLE and _might_be(cast(Hashable, type(obj)), "pydantic")
