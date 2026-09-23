def _get_aten_graph_module_for_pattern(
    pattern: Callable,
    example_inputs: tuple[Any, ...],
    is_cuda: bool = False,
    **kwargs,
) -> GraphModule:
    """
    Convert the pattern to an FX graph with decomposed aten ops.
    """
    if is_cuda:
        example_inputs = tuple(
            [x.cuda() if isinstance(x, torch.Tensor) else x for x in example_inputs]
        )

    aten_pattern = torch.export.export_for_training(
        pattern,  # type: ignore[arg-type]
        example_inputs,
        kwargs,
        strict=True,
    ).module()

    aten_pattern.graph.eliminate_dead_code()  # type: ignore[operator, union-attr]
    aten_pattern.recompile()  # type: ignore[operator]

    # ep.module() adds copy_ nodes for the mutated inputs.
    # For patterns, it doesn't matter
    for node in aten_pattern.graph.nodes:  # type: ignore[union-attr]
        if (
            node.op == "call_function"
            and node.target == torch.ops.aten.copy_.default
            and len(node.users) == 0
        ):
            aten_pattern.graph.erase_node(node)  # type: ignore[operator, union-attr]

    aten_pattern.graph.eliminate_dead_code()  # type: ignore[operator, union-attr]
    aten_pattern.recompile()  # type: ignore[operator]

    return aten_pattern  # type: ignore[return-value]
