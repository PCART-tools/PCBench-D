def track_tensor(
    tensor: Tensor, proxy: Proxy, *, constant: Optional[Tensor], tracer: _ProxyTracer
) -> None:
    def try_set_proxy_slot(
        outer_s: IntLikeType,
        proxy_callable: Callable[Concatenate[PySymType, _P], Proxy],
        *args: _P.args,
        **kwargs: _P.kwargs,
    ) -> None:
        assert callable(proxy_callable)
        if isinstance(outer_s, SymInt):
            with _enable_thunkify(tracer):
                set_proxy_slot(
                    outer_s,
                    tracer,
                    thunkify(tracer, proxy_callable, outer_s, *args, **kwargs),
                )

    # The basic idea is that we need to associate each tensor/SymInt
    # with a Proxy.  How do we setup this association?  We just store
    # the proxy on the proxy slot of the object, keyed on the tracer
    # (so that if we have multiple tracers at the same time, they
    # don't clobber each other.)
    for i, s in enumerate(tensor.shape):
        try_set_proxy_slot(
            s,
            lambda x, i: set_meta(
                tracer.create_proxy(
                    "call_function", torch.ops.aten.sym_size.int, (proxy, i), {}
                ),
                x,
            ),
            i,
        )

    if not is_sparse_any(tensor):
        for i, s in enumerate(tensor.stride()):
            try_set_proxy_slot(
                s,
                lambda x, i: set_meta(
                    tracer.create_proxy(
                        "call_function", torch.ops.aten.sym_stride.int, (proxy, i), {}
                    ),
                    x,
                ),
                i,
            )

    try_set_proxy_slot(
        tensor.numel(),
        lambda x: set_meta(
            tracer.create_proxy(
                "call_function", torch.ops.aten.sym_numel.default, (proxy,), {}
            ),
            x,
        ),
    )
    if not is_sparse_any(tensor):
        try_set_proxy_slot(
            tensor.storage_offset(),
            lambda x: set_meta(
                tracer.create_proxy(
                    "call_function",
                    torch.ops.aten.sym_storage_offset.default,
                    (proxy,),
                    {},
                ),
                x,
            ),
        )
    set_proxy_slot(tensor, tracer, _ProxyTensor(proxy, constant))
