def _invoke_rpc(rref, rpc_api, func_name, timeout, *args, **kwargs):
    # Since rref._get_type can potentially issue an RPC, it should respect the
    # passed in timeout here.
    rref_type = rref._get_type(timeout=timeout)

    _invoke_func = _local_invoke
    # Bypass ScriptModules when checking for async function attribute.
    bypass_type = issubclass(rref_type, torch.jit.ScriptModule) or issubclass(
        rref_type, torch._C.ScriptModule
    )
    if not bypass_type:
        func = getattr(rref_type, func_name)
        if hasattr(func, "_wrapped_async_rpc_function"):
            _invoke_func = _local_invoke_async_execution

    return rpc_api(
        rref.owner(),
        _invoke_func,
        args=(rref, func_name, args, kwargs),
        timeout=timeout
    )
