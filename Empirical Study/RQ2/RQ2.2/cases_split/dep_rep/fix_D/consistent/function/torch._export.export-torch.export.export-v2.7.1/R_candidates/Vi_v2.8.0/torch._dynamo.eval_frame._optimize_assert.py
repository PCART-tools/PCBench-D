def _optimize_assert(
    rebuild_ctx: Callable[[], OptimizeContext],
    backend,
    *,
    hooks=Hooks(None, None, None),
    export=False,
    export_constraints=None,
    dynamic=None,
    package=None,
):
    """
    The same as `torch._dynamo.optimize(backend, nopython=True)`
    """
    backend = get_compiler_fn(backend)

    # Find if backend has any extra context manager
    backend_ctx_ctor = getattr(backend, "backend_ctx_ctor", null_context)

    return _optimize_catch_errors(
        convert_frame.convert_frame_assert(
            backend,
            export=export,
            export_constraints=export_constraints,
            package=package,
        ),
        hooks,
        backend_ctx_ctor,
        export=export,
        dynamic=dynamic,
        rebuild_ctx=rebuild_ctx,
        package=package,
    )
