def maybe_handle_decomp(
    proxy_mode: ProxyTorchDispatchMode,
    op: OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    from torch._inductor.compiler_bisector import CompilerBisector

    if op in CURRENT_DECOMPOSITION_TABLE:
        if CompilerBisector.disable_subsystem(
            "aot_eager_decomp_partition", "decomposition", lambda: repr(op)
        ):
            return NotImplemented

        with proxy_mode:
            proxy_mode.decomp_layers += 1
            out = CURRENT_DECOMPOSITION_TABLE[op](*args, **kwargs)
            proxy_mode.decomp_layers -= 1
            return out

    return NotImplemented
