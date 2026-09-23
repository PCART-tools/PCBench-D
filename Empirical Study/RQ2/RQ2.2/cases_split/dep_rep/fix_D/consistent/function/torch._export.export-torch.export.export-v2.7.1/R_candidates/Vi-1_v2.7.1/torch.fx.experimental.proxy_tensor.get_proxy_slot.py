def get_proxy_slot(
    obj: Union[Tensor, _AnyScriptObjectType, PySymType],
    tracer: _ProxyTracer,
    default: object = no_default,
    transform: Callable = lambda x: x,
) -> object:
    tracker: Any
    if isinstance(obj, Tensor):
        tracker = tracer.tensor_tracker
    elif isinstance(obj, _AnyScriptObject):
        tracker = tracer.script_object_tracker
    else:
        assert isinstance(obj, py_sym_types), type(obj)
        tracker = tracer.symnode_tracker

    if obj not in tracker:
        # Last ditch
        if isinstance(obj, py_sym_types) and obj.node.expr in tracer.sympy_expr_tracker:
            value = tracer.sympy_expr_tracker[obj.node.expr]
        else:
            if isinstance(default, _NoDefault):
                raise RuntimeError(
                    f"{obj} ({id(obj)})is not tracked with proxy for {tracer}"
                )
            return default
    else:
        value = tracker[obj]
    res = transform(value)
    return res
