def get_stack_traces(gm) -> list[Optional[str]]:
    output = output_node(gm)
    assert len(output.args) == 1
    return [
        (arg.stack_trace if isinstance(arg, torch.fx.node.Node) else None)
        for arg in output.args[0]
    ]
