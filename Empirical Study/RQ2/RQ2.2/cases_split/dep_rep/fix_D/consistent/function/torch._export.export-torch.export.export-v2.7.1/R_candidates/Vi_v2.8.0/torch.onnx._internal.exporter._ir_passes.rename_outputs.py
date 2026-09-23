def rename_outputs(model: ir.Model, new_names: Sequence[str]) -> None:
    for output, new_name in zip(model.graph.outputs, new_names):
        output.metadata_props["pkg.torch.onnx.original_node_name"] = str(output.name)
        output.name = new_name
