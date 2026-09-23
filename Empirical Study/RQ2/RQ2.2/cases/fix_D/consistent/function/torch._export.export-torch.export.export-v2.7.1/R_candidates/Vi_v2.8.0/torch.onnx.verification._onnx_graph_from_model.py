def _onnx_graph_from_model(
    model: torch.nn.Module | torch.jit.ScriptModule,
    args: tuple[Any, ...],
    kwargs: Mapping[str, Any],
    export_options: _experimental.ExportOptions,
) -> _C.Graph:
    """As part of the ONNX export steps, export an ONNX JIT graph from a PyTorch model.

    Args:
        model: See :func:`check_export_model_diff`.
        args: See :func:`check_export_model_diff`.
        kwargs: See :func:`check_export_model_diff`.
        export_options: See :func:`check_export_model_diff`.

    Returns:
        onnx_graph (_C.Graph): An ONNX JIT graph.
    """
    # TODO: refactor utils.py to remove duplicated code of context setup. See #78834
    opset_version = export_options.opset_version
    operator_export_type = export_options.operator_export_type
    export_modules_as_functions = export_options.export_modules_as_functions
    training = export_options.training
    verbose = export_options.verbose
    dynamic_axes = export_options.dynamic_axes
    input_names = export_options.input_names
    output_names = export_options.output_names

    if opset_version is None:
        opset_version = _constants.ONNX_DEFAULT_OPSET

    utils._setup_trace_module_map(model, export_modules_as_functions)

    if not operator_export_type:
        operator_export_type = _C_onnx.OperatorExportTypes.ONNX

    GLOBALS.export_onnx_opset_version = opset_version
    GLOBALS.operator_export_type = operator_export_type

    with utils.exporter_context(model, training, verbose):
        do_constant_folding = utils._decide_constant_folding(
            export_options.do_constant_folding, operator_export_type, training
        )

        if dynamic_axes is None:
            dynamic_axes = {}
        utils._validate_dynamic_axes(dynamic_axes, model, input_names, output_names)

        export_inputs = _prepare_input_for_export(args, kwargs)
        export_inputs = utils._decide_input_format(model, export_inputs)
        onnx_graph, _, _ = utils._model_to_graph(
            model,
            export_inputs,
            verbose,
            input_names,
            output_names,
            operator_export_type,
            do_constant_folding,
            training=training,
            dynamic_axes=dynamic_axes,
        )

        return onnx_graph
