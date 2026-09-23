def autograd_cache_key(
    gm: torch.fx.GraphModule,
    example_inputs,
    config: AOTConfig,
    fx_config: _CompileFxKwargs,
    # TODO: add args and parameters
) -> tuple[str, list[str]]:
    """
    Generate a unique hash of the FX graph for caching.
    """
    check_cacheable(gm)
    if has_triton_package():
        # Due to https://github.com/triton-lang/triton/issues/3729,
        # if triton is < 3.2.0, AOTAutogradCache may cause us to
        # attempt to load a cache entry without initializing
        # the CUDA context on the autograd thread.

        # Without caching, we naturally do this initialization when
        # tracing through the graph with the autograd engine.
        import triton

        if triton.__version__ < "3.2.0":
            raise BypassAOTAutogradCache("AOTAutogradCache requires triton 3.2.0")

    details = AOTAutogradCacheDetails(gm, example_inputs, config, fx_config)
    pickler = AOTAutogradCachePickler(gm)
    # The prefix distinguishes among the other kinds of objects we cache
    key = "a" + pickler.get_hash(details)
    debug_lines = pickler.debug_lines(details)
    log.debug(
        "Autograd graph cache hash details for key %s:\n%s",
        key,
        LazyString(lambda: "\n".join(debug_lines)),
    )
    return key, debug_lines
