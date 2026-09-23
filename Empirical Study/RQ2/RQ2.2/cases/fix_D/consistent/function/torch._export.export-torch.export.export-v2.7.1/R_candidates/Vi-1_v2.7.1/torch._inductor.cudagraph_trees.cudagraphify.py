def cudagraphify(
    model: ModelType,
    inputs: list[InputType],
    static_input_idxs: Sequence[int] = (),
    *,
    device_index: int,
    is_backward: bool,
    is_inference: bool,
    stack_traces: Optional[StackTraces] = None,
    constants: tuple[torch.Tensor, ...] = (),
    placeholders: tuple[PlaceholderInfo, ...] = (),
    mutated_input_idxs: tuple[int, ...] = (),
    compile_id: Optional[CompileId] = None,
) -> tuple[ModelType, OutputType]:
    assert not (is_backward and is_inference)
    mode = (
        CompilationMode.BACKWARD
        if is_backward
        else (CompilationMode.INFERENCE if is_inference else CompilationMode.FORWARD)
    )

    with dynamo_timed_cudagraph(
        "cudagraphify.get_container", compile_id, mode, dynamo_compile=True
    ):
        manager = get_container(device_index).get_tree_manager()

    with dynamo_timed_cudagraph("CUDAGraphTreeManager.add_function", compile_id, mode):
        return manager.add_function(
            model,
            inputs,
            static_input_idxs,
            stack_traces,
            mode,
            constants,
            placeholders,
            mutated_input_idxs,
            compile_id,
        )
