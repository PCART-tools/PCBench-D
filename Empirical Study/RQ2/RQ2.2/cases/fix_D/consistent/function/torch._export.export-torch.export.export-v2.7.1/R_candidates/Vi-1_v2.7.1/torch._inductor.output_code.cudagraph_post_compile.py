def cudagraph_post_compile(
    example_inputs: Sequence[InputType],
    compiled_graph: CompiledFxGraph,
    cudagraphs: BoxedBool,
    constants: dict[str, torch.Tensor],
) -> None:
    """
    Checks for any reasons not to run cudagraphs and then
    runs it on compiled_graph.
    Mutates the `compiled_graph.current_callable` and `cudagraphs`
    """
    assert compiled_graph.current_callable is not None
    assert compiled_graph.cudagraph_info is not None
    cached_info = compiled_graph.cudagraph_info
    cudagraph_fail_reasons = cached_info.cudagraph_fail_reasons
    boxed_forward_device_index = compiled_graph.boxed_forward_device_index
    is_inference = compiled_graph.fx_kwargs["is_inference"]
    is_backward = compiled_graph.fx_kwargs["is_backward"]

    if not cudagraph_fail_reasons:
        fx_kwargs = compiled_graph.fx_kwargs
        static_input_idxs = fx_kwargs["static_input_idxs"]

        placeholders = cached_info.placeholders
        stack_traces = cached_info.stack_traces
        if not config.triton.cudagraph_trees:
            # Force specialize all inputs so that CUDA graphs will work
            for t in example_inputs:
                if isinstance(t, torch.SymInt):
                    int(t)  # guard

        if (
            boxed_forward_device_index is not None
            and not is_inference
            and not is_backward
        ):
            boxed_forward_device_index.set(next(iter(compiled_graph.device_idxs)))

        from .compile_fx import cudagraphify

        current_callable = compiled_graph.current_callable
        assert current_callable is not None
        compiled_graph.current_callable = cudagraphify(
            current_callable,
            static_input_idxs=static_input_idxs or (),
            device_index=next(iter(compiled_graph.device_idxs)),
            stack_traces=stack_traces,
            is_backward=is_backward,
            is_inference=is_inference,
            constants=tuple(constants.values()),
            placeholders=placeholders,
            mutated_input_idxs=tuple(compiled_graph.mutated_input_idxs),
        )

    else:
        BoxedBool.disable(cudagraphs)

        # See [Backward Generation Handling]
        # if cudagraph'd the forward and set the device, we need to let the cudagraph manager
        # know we are we running the backward even if we will not run it in cudagraphs
        if is_backward and config.triton.cudagraph_trees:
            assert boxed_forward_device_index is not None
            assert boxed_forward_device_index.value is not None
            compiled_graph_callable = compiled_graph.current_callable

            manager = torch._inductor.cudagraph_trees.get_manager(
                boxed_forward_device_index.value, create_if_none_exists=False
            )
            # should already exist from forward
            assert manager is not None

            def compiled_artifact(new_inputs: list[Any]) -> Callable[..., Any]:
                manager.set_to_running_backward()  # type: ignore[union-attr]
                return compiled_graph_callable(new_inputs)

            compiled_graph.current_callable = compiled_artifact

        if "cuda" in compiled_graph.device_types:
            # prefer better disable_cudagraphs_reason bc stack trace
            # TODO: migrate all disable reasons to stack trace, refactor
            if compiled_graph.disabled_cudagraphs_reason:
                log_cudagraph_skip_and_bump_counter(
                    compiled_graph.disabled_cudagraphs_reason
                )
            else:
                log_cudagraph_skip_and_bump_counter(
                    f"skipping cudagraphs due to {cudagraph_fail_reasons}"
                )
