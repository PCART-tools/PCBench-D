@auto_functionalized_v2.py_impl(ProxyTorchDispatchMode)
def auto_functionalized_v2_proxy(
    mode,
    _mutable_op: OpOverload,
    **kwargs: dict[str, Any],
) -> tuple[Any, tuple[Tensor, ...]]:
    with disable_proxy_modes_tracing():
        out = auto_functionalized_v2(_mutable_op, **kwargs)

    proxy_kwargs = pytree.tree_map(mode.tracer.unwrap_proxy, kwargs)
    out_proxy = mode.tracer.create_proxy(
        "call_function",
        auto_functionalized_v2,
        (_mutable_op,),
        proxy_kwargs,
    )
    result = track_tensor_tree(out, out_proxy, constant=None, tracer=mode.tracer)
    return result
