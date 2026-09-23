@contextlib.contextmanager
def _set_graph_outputs(
    graph: ir.Graph,
    outputs: list[ir.Value],
):
    """Temporarily set the outputs of the graph.

    Args:
        graph: The graph to set the outputs for.
        outputs: The outputs to set.
    """
    original_outputs = graph.outputs.copy()
    graph.outputs.clear()
    graph.outputs.extend(outputs)
    try:
        yield
    finally:
        graph.outputs.clear()
        graph.outputs.extend(original_outputs)
