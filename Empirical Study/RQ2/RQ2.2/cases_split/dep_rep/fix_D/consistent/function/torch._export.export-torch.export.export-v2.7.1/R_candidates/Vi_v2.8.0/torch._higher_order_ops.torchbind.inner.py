@call_torchbind.py_impl(ProxyTorchDispatchMode)
def inner(mode, *args, **kwargs):
    proxy_args = pytree.tree_map(mode.tracer.unwrap_proxy, args)
    proxy_kwargs = pytree.tree_map(mode.tracer.unwrap_proxy, kwargs)

    out_proxy = mode.tracer.create_proxy(
        "call_function",
        call_torchbind,
        proxy_args,
        proxy_kwargs,
    )
    out = call_torchbind(*args, **kwargs)

    obj, method, *_rest_args = args
    if isinstance(obj, torch.ScriptObject):
        ns, class_name = _ns_and_class_name(
            obj._type().qualified_name()  # type: ignore[attr-defined]
        )
        log.warning(
            "Tracing torchbind method %s.%s with real ScriptObject. This may"
            " cause the original object being mutated. If this is not intended,"
            ' You can register a fake class with torch._library.register_fake_class("%s::%s").',
            class_name,
            method,
            ns,
            class_name,
        )

    ret = track_tensor_tree(out, out_proxy, constant=None, tracer=mode.tracer)
    if "val" not in out_proxy.node.meta:
        assert out is None or isinstance(
            out, (int, float, bool)
        ), "Currently, only these constant dtypes are supported to be returned from torchbind methods."
        out_proxy.node.meta["val"] = out
    return ret
