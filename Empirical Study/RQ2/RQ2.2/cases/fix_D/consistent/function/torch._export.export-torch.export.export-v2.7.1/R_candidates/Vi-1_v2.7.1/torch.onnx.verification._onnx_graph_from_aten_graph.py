def _onnx_graph_from_aten_graph(
    graph: torch.Graph,
    export_options: _experimental.ExportOptions,
    params_dict: dict[str, Any] | None = None,
) -> tuple[torch.Graph, dict[str, Any]]:
    if params_dict is None:
        params_dict = {}
    operator_export_type = export_options.operator_export_type
    dynamic_axes = export_options.dynamic_axes or {}
    input_names = export_options.input_names
    training = export_options.training
    do_constant_folding = export_options.do_constant_folding
    opset_version = export_options.opset_version or _constants.ONNX_DEFAULT_OPSET

    GLOBALS.export_onnx_opset_version = opset_version
    GLOBALS.operator_export_type = operator_export_type

    do_constant_folding = utils._decide_constant_folding(
        do_constant_folding, operator_export_type, training
    )

    # TODO: Below is doing aten graph to onnx. It should be abstracted as a
    # function in torch/onnx/utils.py.
    graph = graph.copy()
    graph = utils._optimize_graph(
        graph,
        operator_export_type,
        params_dict=params_dict,
        dynamic_axes=dynamic_axes,
        input_names=input_names,
    )

    if training is None or training == _C_onnx.TrainingMode.EVAL:
        params_dict = torch._C._jit_pass_onnx_eval_peephole(graph, params_dict)

    if (
        do_constant_folding
        and opset_version >= _constants.ONNX_CONSTANT_FOLDING_MIN_OPSET
    ):
        params_dict = _C._jit_pass_onnx_constant_fold(graph, params_dict, opset_version)
        _C._jit_pass_dce_allow_deleting_nodes_with_side_effects(graph)

    if GLOBALS.onnx_shape_inference:
        _C._jit_pass_onnx_graph_shape_type_inference(graph, params_dict, opset_version)

    params_dict = _C._jit_pass_onnx_eliminate_unused_items(graph, params_dict)

    # For ONNX opset < 9, constants only have three data types: float16, float, double.
    # In this pass transform constants of other data types to float/double + cast operator.
    if opset_version < 9:
        _C._jit_pass_onnx_cast_all_constant_to_floating(graph)

    params_dict = _C._jit_pass_filter_non_tensor_arguments(params_dict)
    _C._jit_decay_packed_param_input_types(graph)

    _C._jit_pass_dce_allow_deleting_nodes_with_side_effects(graph)

    if export_options.verbose:
        print("ONNX graph: ", graph)

    return graph, params_dict
