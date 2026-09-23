def _aot_export_function(
    func: Callable,
    args,
    *,
    num_params_buffers: int = 0,
    decompositions: Optional[dict] = None,
    # If we're exporting a joint graph and we don't want any tangent inputs in the graph
    # (because we are backpropping through a scalar 1 loss),
    # we need to explicitly specify not to include tangents in the graph.
    # It's not enough just to check that our tangent is a scalar, since we also
    # need to know if it is a 1 (no need to make it a graph input), or something else
    # (requiring it to be a graph input).
    # We don't know this info at trace time though, so we need to make it an explicit config.
    no_tangents: bool = False,
    pre_dispatch: bool = False,
    # If None, `dynamic_shapes` will be infered from inputs, but the inferred result might be wrong.
    dynamic_shapes: Optional[bool] = None,
    kwargs=None,
) -> tuple[torch.fx.GraphModule, ViewAndMutationMeta, pytree.TreeSpec, pytree.TreeSpec]:
    kwargs = kwargs or {}

    flat_fn, out_spec = create_tree_flattened_fn(func, args, kwargs)
    flat_args, in_spec = pytree.tree_flatten((args, kwargs))

    fake_mode = None
    if dynamic_shapes is None:
        # Try to infer `dynamic_shapes from inputs and graph nodes
        fake_mode = detect_fake_mode(flat_args)
        if (
            fake_mode is None
            and hasattr(func, "_orig_mod")
            and isinstance(func._orig_mod, torch.fx.GraphModule)
        ):
            vals = [
                node.meta["val"]
                for node in func._orig_mod.graph.nodes
                if "val" in node.meta
            ]
            fake_mode = detect_fake_mode(vals)
        dynamic_shapes = fake_mode is not None and fake_mode.shape_env is not None

    # The export use case doesn't care about several bits of AOTConfig
    # (1) compilers (we just export the graph)
    # (2) partitioners (export is only full graph, user can partition themselves)
    aot_config = AOTConfig(
        fw_compiler=None,
        bw_compiler=None,
        inference_compiler=None,
        partition_fn=None,
        decompositions=decompositions,
        num_params_buffers=num_params_buffers,
        aot_id=next(AOT_COUNTER),
        # For now there's no use case involving keeping input mutations in the graph
        # (which we can only do in the inference case anyway).
        # We can add this later if we need to.
        keep_inference_input_mutations=False,
        dynamic_shapes=dynamic_shapes,
        aot_autograd_arg_pos_to_source=None,
        is_export=True,
        no_tangents=no_tangents,
        pre_dispatch=pre_dispatch,
    )
    if fake_mode is None:
        fake_mode, shape_env = construct_fake_mode(flat_args, aot_config)
    else:
        shape_env = fake_mode.shape_env
    fake_flat_args = process_inputs(flat_args, aot_config, fake_mode, shape_env)

    fx_g, meta = create_aot_dispatcher_function(
        flat_fn,
        fake_flat_args,
        aot_config,
        fake_mode,
        shape_env,
    )
    return fx_g, meta, in_spec, out_spec.spec
