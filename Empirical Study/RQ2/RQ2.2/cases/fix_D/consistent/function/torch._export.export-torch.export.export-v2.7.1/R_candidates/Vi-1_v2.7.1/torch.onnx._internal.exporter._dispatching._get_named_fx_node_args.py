def _get_named_fx_node_args(node: torch.fx.Node) -> dict[str, torch.fx.node.Argument]:
    assert hasattr(node.target, "_schema")
    torch_schema: torch.FunctionSchema = node.target._schema  # type: ignore[union-attr]
    node_args = {}
    for arg, schema_arg in zip(node.args, torch_schema.arguments):
        node_args[schema_arg.name] = arg

    node_args.update(node.kwargs)
    return node_args
