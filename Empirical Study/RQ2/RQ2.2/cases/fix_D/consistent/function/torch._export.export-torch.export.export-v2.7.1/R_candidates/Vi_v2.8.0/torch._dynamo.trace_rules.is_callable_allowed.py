def is_callable_allowed(obj) -> bool:
    _maybe_init_lazy_module(obj)
    return id(obj) in _allowed_callable_ids
