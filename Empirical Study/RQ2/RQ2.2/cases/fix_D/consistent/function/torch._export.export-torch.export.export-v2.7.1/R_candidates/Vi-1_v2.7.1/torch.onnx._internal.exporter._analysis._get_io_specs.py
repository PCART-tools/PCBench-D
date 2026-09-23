def _get_io_specs(exported_program: torch.export.ExportedProgram) -> tuple[dict, dict]:
    """Get the input and output specs of the exported program."""

    nodes: dict[str, torch.fx.Node] = {
        node.name: node for node in exported_program.graph.nodes
    }
    user_inputs = [
        spec
        for spec in exported_program.graph_signature.input_specs
        if spec.kind == graph_signature.InputKind.USER_INPUT
    ]
    user_outputs = [
        spec
        for spec in exported_program.graph_signature.output_specs
        if spec.kind == graph_signature.OutputKind.USER_OUTPUT
    ]
    inputs: dict[str, torch._export.serde.schema.TensorMeta] = {}
    outputs: dict[str, torch._export.serde.schema.TensorMeta] = {}
    for spec in user_inputs:
        if isinstance(spec.arg, graph_signature.ConstantArgument):
            continue
        name = spec.arg.name
        # FIXME: tensor_meta is None sometimes when the exported program still knows the shape/type
        inputs[name] = nodes[name].meta["tensor_meta"]
    for spec in user_outputs:
        if isinstance(spec.arg, graph_signature.ConstantArgument):
            continue
        name = spec.arg.name
        outputs[name] = nodes[name].meta["tensor_meta"]
    return inputs, outputs
