def _traced_graph_from_model(
    model: torch.nn.Module | torch.jit.ScriptModule,
    args: tuple[Any, ...],
    kwargs: Mapping[str, Any],
    export_options: _experimental.ExportOptions,
) -> _C.Graph:
    """As part of the ONNX export steps, create a traced JIT graph from a PyTorch model.

    Args:
        model: See :func:`check_export_model_diff`.
        args: See :func:`check_export_model_diff`.
        kwargs: See :func:`check_export_model_diff`.
        export_options: See :func:`check_export_model_diff`.

    Returns:
        jit_graph (_C.Graph): A traced JIT graph.
    """
    training = export_options.training
    verbose = export_options.verbose

    with utils.exporter_context(model, training, verbose):
        export_inputs = _prepare_input_for_export(args, kwargs)
        model = utils._pre_trace_quant_model(model, export_inputs)
        jit_graph, _, _, _ = utils._create_jit_graph(model, export_inputs)
        return jit_graph
