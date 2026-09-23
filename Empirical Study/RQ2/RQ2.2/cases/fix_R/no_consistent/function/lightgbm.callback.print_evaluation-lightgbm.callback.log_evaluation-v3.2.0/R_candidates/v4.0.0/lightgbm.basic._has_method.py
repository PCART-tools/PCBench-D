def _has_method(logger: Any, method_name: str) -> bool:
    return callable(getattr(logger, method_name, None))
