def fetch_object_proxy(
    tracer: _ProxyTracer, t: Union[Tensor, _AnyScriptObjectType, PySymType]
) -> object:
    return get_proxy_slot(t, tracer, t)
