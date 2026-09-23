def _handle_output_node(
    node: torch.fx.Node,
    node_name_to_values: dict[str, ir.Value | Sequence[ir.Value]],
    graph_like: ir.Graph | ir.Function,
) -> None:
    """Handle an output node by adding the output to the graph's outputs.

    Args:
        node: The FX node to translate.
        node_name_to_values: A mapping of FX node names to their produced ONNX ``Value``.
        graph_like: The ONNX graph at construction.
    """
    # node.args[0] can be a tuple with more than one elements. This happens when,
    # for example, a subgraph has multiple outputs. We flatten them all as ONNX graph outputs
    for output in node.args[0]:  # type: ignore[index,union-attr]
        output_value_name = output.name  # type: ignore[union-attr]
        assert isinstance(output_value_name, str), (
            f"Bug: Expected {output_value_name!r} to be a string"
        )
        values = node_name_to_values[output_value_name]
        if isinstance(values, Sequence):
            graph_like.outputs.extend(values)
            return
        graph_like.outputs.append(values)
