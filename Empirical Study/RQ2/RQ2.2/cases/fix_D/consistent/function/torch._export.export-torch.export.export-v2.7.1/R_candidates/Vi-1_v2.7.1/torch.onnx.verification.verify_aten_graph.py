@typing_extensions.deprecated(
    "torch.onnx.verification.* is deprecated. Consider using torch.onnx.export(..., dynamo=True) "
    "and use ONNXProgram to test the ONNX model"
)
def verify_aten_graph(
    graph: torch.Graph,
    input_args: tuple[Any, ...],
    export_options: _experimental.ExportOptions,
    params_dict: dict[str, Any] | None = None,
    verification_options: VerificationOptions | None = None,
) -> tuple[AssertionError | None, torch.Graph, _OutputsType, _OutputsType]:
    """Verify aten graph export to ONNX against original PyTorch model.

    .. deprecated:: 2.7
        Consider using ``torch.onnx.export(..., dynamo=True)`` and use the returned
        ``ONNXProgram`` to test the ONNX model.
    """
    if verification_options is None:
        verification_options = VerificationOptions()
    if params_dict is None:
        params_dict = {}

    original_jit_graph = graph
    graph = graph.copy()

    # Execute aten graph and get reference torch jit outputs.
    graph_inputs = list(graph.inputs())
    jit_inputs = tuple([arg for arg in input_args if arg is not None])
    weights = [params_dict[v.debugName()] for v in graph_inputs[len(jit_inputs) :]]
    assert all(w is not None for w in weights)
    # TODO: Only copy the argument if mutation is detected in Graph.
    jit_inputs = copy.deepcopy(jit_inputs)
    jit_input_and_parameters = jit_inputs + tuple(weights)
    jit_outs = torch._C._jit_interpret_graph(graph, jit_input_and_parameters)  # type: ignore[attr-defined]
    if not isinstance(jit_outs, (list, tuple)):
        jit_outs = [jit_outs]

    # Convert aten graph to onnx graph.
    graph, onnx_params_dict = _onnx_graph_from_aten_graph(
        graph, export_options, params_dict
    )

    proto, export_map = _onnx_proto_from_onnx_graph(
        graph, export_options, onnx_params_dict
    )
    model_f: str | io.BytesIO = io.BytesIO()
    onnx_proto_utils._export_file(proto, model_f, export_map)

    # NOTE: Verification is unstable. Try catch to emit information for debugging.
    try:
        # NOTE: Input might be dce'ed, so we need to remove those from the input args.
        new_input_names = {v.debugName() for v in graph.inputs()}
        new_input_args = []
        for v, arg in zip(original_jit_graph.inputs(), input_args):
            if v.debugName() in new_input_names:
                new_input_args.append(arg)
        input_args = tuple(new_input_args)

        onnx_inputs = _prepare_input_for_onnx(
            input_args,
            {},
            verification_options.remained_onnx_input_idx,
            verification_options.flatten,
        )

        onnx_session = _onnx_backend_session(model_f, verification_options.backend)
        onnx_outs = _run_onnx(onnx_session, onnx_inputs)
        del onnx_session  # To free device memory

        try:
            _compare_onnx_pytorch_outputs(
                onnx_outs=onnx_outs,
                pt_outs=jit_outs,
                options=verification_options,
            )
        except AssertionError as e:
            return e, graph, jit_outs, onnx_outs

        return None, graph, jit_outs, onnx_outs

    except Exception as e:
        print("Unexpected error during verification.")
        print("jit graph: ", original_jit_graph)
        print("onnx graph: ", graph)
        raise e
