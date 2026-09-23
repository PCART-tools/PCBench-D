def _invoke_rpc(rref, rpc_api, func_name, timeout, *args, **kwargs):
    def _rref_type_cont(rref_fut):
        rref_type = rref_fut.value()

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
            timeout=timeout,
        )

    rref_fut = rref._get_type(timeout=timeout, blocking=False)

    if rpc_api != rpc_async:
        rref_fut.wait()
        return _rref_type_cont(rref_fut)
    else:
        # A little explanation on this.
        # rpc_async returns a Future pointing to the return value of `func_name`, it returns a `Future[T]`
        # Calling _rref_type_cont from the `then` lambda causes Future wrapping. IOW, `then` returns a `Future[Future[T]]`
        # To address that, we return a Future that is completed with the result of the async call.
        result: Future = Future()

        def _wrap_rref_type_cont(fut):
            try:
                _rref_type_cont(fut).then(_complete_op)
            except BaseException as ex:
                result.set_exception(ex)

        def _complete_op(fut):
            try:
                result.set_result(fut.value())
            except BaseException as ex:
                result.set_exception(ex)

        rref_fut.then(_wrap_rref_type_cont)
        return result
