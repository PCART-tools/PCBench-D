def standalone_compile(
    gm: torch.fx.GraphModule,
    example_inputs: list[InputType],
    *,
    dynamic_shapes: Literal[
        "from_example_inputs", "from_tracing_context", "from_graph"
    ] = "from_graph",
    options: Optional[dict[str, Any]] = None,
) -> CompiledArtifact:
    """
    Precompilation API for inductor.

    .. code-block:: python

        compiled_artifact = torch._inductor.standalone_compile(gm, args)
        compiled_artifact.save(path=path, format="binary")

        # Later on a new process
        loaded = torch._inductor.CompiledArtifact.load(path=path, format="binary")
        compiled_out = loaded(*args)

    Args:
        gm: Graph Module
        example_inputs: Inputs for the graph module
        dynamic_shapes: If "from_graph" (default), we will use the dynamic
            shapes in the passed-in graph module.
            If "from_tracing_context", we use the dynamic shape info in the
            ambient tracing context.
            If "from_example_inputs", we will specialize the graph on the
            example_inputs.
        options: Inductor compilation options

    Returns:
        CompiledArtifact that can be saved to disk or invoked directly.
    """
    from .standalone_compile import standalone_compile

    options = options if options else {}
    return standalone_compile(
        gm, example_inputs, dynamic_shapes=dynamic_shapes, options=options
    )
