def standalone_compile(
    gm: GraphModule,
    example_inputs: Sequence[InputType],
    *,
    dynamic_shapes: Any,
    options: Any,
) -> CompiledArtifact:
    from torch.compiler._cache import CacheArtifactManager

    from .compile_fx import compile_fx

    ignore_shape_env = False
    if dynamic_shapes == "from_example_inputs":
        fake_mode = FakeTensorMode(shape_env=ShapeEnv())
        # tells compile_fx to ignore the shape_envs on the ambient context
        # and the graph_module.
        ignore_shape_env = True
    elif dynamic_shapes == "from_tracing_context":
        # Reuse fake_mode from the TracingContext.
        # NB: The TracingContext only exists if we're currently in a torch.compile backend.
        context = torch._guards.TracingContext.get()
        fake_mode = context.fake_mode
    elif dynamic_shapes == "from_graph":
        fake_mode = FakeTensorMode(shape_env=ShapeEnv())
        # Strategy: find a FakeTensor in the graph output, grab its FakeTensorMode.
        # The graph passed to standalone_compile must be an Inductor-approved graph,
        # which means that there is at least one Tensor output and the output node
        # contains a flat list of Tensors.
        last_node = next(iter(reversed(gm.graph.nodes)))
        assert last_node.op == "output"
        assert len(last_node.args) == 1
        for node in last_node.args[0]:
            if "example_value" in node.meta:
                maybe_tensor = node.meta["example_value"]
                if isinstance(maybe_tensor, torch._subclasses.fake_tensor.FakeTensor):
                    fake_mode = maybe_tensor.fake_mode
    else:
        raise ValueError(
            f"standalone_compile got unsupported `dynamic_shapes` value: dynamic_shapes={dynamic_shapes}."
        )

    context = torch._guards.TracingContext(fake_mode)
    with (
        torch._guards.tracing(context),
        CacheArtifactManager.with_fresh_cache(),
        config.patch("triton.autotune_at_compile_time", True),
    ):
        # compile_fx can mutate gm
        gm = copy.deepcopy(gm)
        compiled_fn = compile_fx(
            gm, example_inputs, ignore_shape_env=ignore_shape_env, **options
        )
        assert callable(compiled_fn)

        artifacts = torch.compiler.save_cache_artifacts()
        if artifacts is None:
            log.warning(
                "standalone_compile artifact generation failed, cannot save. "
                "Run with TORCH_LOGS=+torch._inductor.codecache to identify the problem"
            )

    return CompiledArtifact(compiled_fn, artifacts)
