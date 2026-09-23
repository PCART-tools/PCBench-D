def reenter_make_fx(fn):
    from torch.fx.experimental.proxy_tensor import _CURRENT_MAKE_FX_TRACER

    @functools.wraps(fn)
    def wrapped(*args):
        assert (
            _CURRENT_MAKE_FX_TRACER is not None
        ), "Cannot reenter make_fx when we're not under a make_fx tracing session"
        return _CURRENT_MAKE_FX_TRACER.trace_subgraph(
            _maybe_run_with_interpreter(fn), *args
        )

    return wrapped
