def _maybe_fake_tracing(fn, inputs: list[Any], pre_dispatch):
    fake_mode = detect_fake_mode(inputs)
    tracing_mode = "real"
    if fake_mode is None:
        fake_mode = nullcontext()
        tracing_mode = "fake"

    # Note: we need to turn off proxy tensor mode to avoid tracing infra
    # code that happens in make_fx e.g. we now call as_strided when wrapping tensor
    # as fake tensor.
    with fake_mode, disable_proxy_modes_tracing():
        gm = make_fx(
            fn,
            tracing_mode=tracing_mode,
            pre_dispatch=pre_dispatch,
            _error_on_data_dependent_ops=False,
        )(*inputs)
        if not isinstance(fake_mode, nullcontext) and fake_mode.shape_env is not None:
            insert_deferred_runtime_asserts(
                gm, fake_mode.shape_env, "hoo_maybe_fake_tracing", export=True
            )
        return gm
