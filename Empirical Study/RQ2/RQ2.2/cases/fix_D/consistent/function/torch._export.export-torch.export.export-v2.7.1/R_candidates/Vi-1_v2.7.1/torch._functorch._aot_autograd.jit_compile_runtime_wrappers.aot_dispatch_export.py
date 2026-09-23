def aot_dispatch_export(
    flat_fn: Callable,
    flat_args: list[Any],
    aot_config: AOTConfig,
    *,
    fw_metadata: ViewAndMutationMeta,
    needs_autograd: bool,
) -> DispatchReturn:
    wrappers = _create_wrappers_for_dispatch(needs_autograd)
    flat_fn, flat_args, fw_metadata = pre_compile(
        wrappers,
        flat_fn,
        flat_args,
        aot_config,
        fw_metadata=fw_metadata,
    )
    if needs_autograd and not aot_config.pre_dispatch:
        graph, _, _ = aot_dispatch_autograd_graph(
            flat_fn, flat_args, aot_config, fw_metadata=fw_metadata
        )
    else:
        graph, _, _ = aot_dispatch_base_graph(
            flat_fn, flat_args, aot_config, fw_metadata=fw_metadata
        )

    # NB: the wrappers that run in pre_compile for export are
    # either a no-op, because they're not needed, or will raise a runtime error,
    # since they don't support export.
    # We still run these wrappers to make sure that they're not needed pre compile,
    # but we technically don't need to run them post compile at all here.
    compiled_fn, fw_metadata = post_compile(
        wrappers, graph, aot_config, runtime_metadata=fw_metadata
    )

    # Therefore, since no wrapperes run, we don't get back a callable - we get back the raw fx graph
    # (either a joint or an inference-only graph)
    assert isinstance(compiled_fn, torch.fx.GraphModule)
    return compiled_fn, fw_metadata
