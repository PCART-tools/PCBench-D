def has_proxy_slot(obj: Tensor, tracer: _ProxyTracer) -> bool:
    assert isinstance(obj, (Tensor, SymNode)), type(obj)
    return bool(get_proxy_slot(obj, tracer, False, lambda _: True))
