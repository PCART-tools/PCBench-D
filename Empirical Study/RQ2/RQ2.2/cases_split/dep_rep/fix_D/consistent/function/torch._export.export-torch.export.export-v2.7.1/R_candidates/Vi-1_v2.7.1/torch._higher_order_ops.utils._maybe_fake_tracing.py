def _maybe_fake_tracing(fn, inputs: list[Any], pre_dispatch):
    fake_mode = detect_fake_mode(inputs)
    tracing_mode = "real"
    if fake_mode is None:
        tracing_mode = "fake"

    # Note: we need to turn off proxy tensor mode to avoid tracing infra
    # code that happens in make_fx e.g. we now call as_strided when wrapping tensor
    # as fake tensor.
    with disable_proxy_modes_tracing():
        return make_fx(
            fn,
            tracing_mode=tracing_mode,
            pre_dispatch=pre_dispatch,
            _error_on_data_dependent_ops=False,
        )(*inputs)
