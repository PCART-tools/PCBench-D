def check_export_model_diff(
    model: torch.nn.Module | torch.jit.ScriptModule,
    test_input_groups: Sequence[tuple[tuple[Any, ...], Mapping[str, Any]]],
    export_options: _experimental.ExportOptions | None = None,
) -> str:
    """Verify exported model discrepancy between different groups of inputs.

    A graph is exported for each group of inputs. The exported graphs are then compared
    to each other, and discrepancies of first pair of nodes are reported. This function
    first checks the jit graph. If no discrepancies were found, it then checks the onnx
    graph.

    Unless otherwise specified, the jit/ONNX graph is expected to be the same, regardless
    of the inputs used for exporting. A discrepancy implies the graph exported is
    not accurate when run on other groups of inputs, which will typically results in
    runtime errors or mismatching output.

    Args:
        model (torch.nn.Module or torch.jit.ScriptModule): The model to be exported.
        test_input_groups (Sequence[Tuple[Tuple[Any, ...], Mapping[str, Any]]]): A sequence
            of input groups to be used to export the model. Each input group is a pair of
            (args, kwargs).
        export_options (_experimental.ExportOptions, optional): An _experimental.ExportOptions
            object that controls the export behavior.

    Returns:
        str: A string containing the diff of the exported models.
    """
    export_options = (
        _experimental.ExportOptions() if export_options is None else export_options
    )

    jit_diff_report = _check_graph_diff(
        model, test_input_groups, export_options, _traced_graph_from_model
    )
    if jit_diff_report:
        return jit_diff_report

    return _check_graph_diff(
        model, test_input_groups, export_options, _onnx_graph_from_model
    )
