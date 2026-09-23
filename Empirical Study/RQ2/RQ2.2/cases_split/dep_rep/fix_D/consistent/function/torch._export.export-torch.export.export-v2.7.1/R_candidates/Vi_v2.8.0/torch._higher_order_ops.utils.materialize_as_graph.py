def materialize_as_graph(
    fn: Callable,
    args: tuple[Any],
    include_key_set: Optional[torch._C.DispatchKeySet] = None,
    exclude_key_set: Optional[torch._C.DispatchKeySet] = None,
    force_enable_grad=False,
) -> torch.fx.GraphModule:
    if include_key_set is None:
        include_key_set = torch._C._dispatch_tls_local_include_set()
    if exclude_key_set is None:
        exclude_key_set = torch._C._dispatch_tls_local_exclude_set()

    @torch._dynamo.disable(recursive=True, reason=None)
    def _materialize_as_graph_inner():
        with suspend_functionalization(), disable_functional_mode():
            with disable_proxy_modes_tracing():
                unfunc_t = [_from_fun(arg) for arg in args]
            with contextlib.ExitStack() as stack:
                stack.enter_context(
                    torch._C._ForceDispatchKeyGuard(include_key_set, exclude_key_set),
                )
                if force_enable_grad:
                    stack.enter_context(torch.enable_grad())
                return _maybe_reenter_make_fx(fn)(*unfunc_t)

    gm = _materialize_as_graph_inner()
    assert gm is not None
    return gm
