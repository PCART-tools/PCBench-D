def _check_graph_diff(
    model: torch.nn.Module | torch.jit.ScriptModule,
    test_input_groups: Sequence[tuple[tuple[Any, ...], Mapping[str, Any]]],
    export_options: _experimental.ExportOptions,
    model_to_graph_func: Callable[
        [
            torch.nn.Module,
            tuple[Any, ...],
            Mapping[str, Any],
            _experimental.ExportOptions,
        ],
        _C.Graph,
    ],
) -> str:
    """Check if graph produced by `model_to_graph_func` is the same across `test_input_groups`.

    Args:
        model: See :func:`check_export_model_diff`.
        test_input_groups: See :func:`check_export_model_diff`.
        export_options: See :func:`check_export_model_diff`.
        model_to_graph_func: A function to convert a PyTorch model to a JIT IR graph.

    Returns:
        graph_diff_report (str): A string representation of the graph difference.
    """
    if len(test_input_groups) < 2:
        raise ValueError("Need at least two groups of test inputs to compare.")

    ref_jit_graph = None
    for args, kwargs in test_input_groups:
        jit_graph = model_to_graph_func(model, args, kwargs, export_options)
        if ref_jit_graph is None:
            ref_jit_graph = jit_graph
            continue

        graph_diff_report = _GraphDiff(ref_jit_graph, jit_graph).diff_report()
        if graph_diff_report:
            return graph_diff_report
    return ""
