def unconvertible_ops(model, args, training=TrainingMode.EVAL, opset_version=None):
    r"""
    Converts the model with operator_export_type set to
    OperatorExportTypes.ONNX_FALLTHROUGH once in order to get a list of
    all the ops that are not supported/implemented by the exporter.

    Args:
        model: Same as corresponding arg to torch.onnx.export.
        args: Same as corresponding arg to torch.onnx.export.
        training: Same as corresponding arg to torch.onnx.export.
        opset_version: Same as corresponding arg to torch.onnx.export.

    Returns:
        Tuple[torch._C.Graph, List[str]], where the list includes the names
          of the unconvertible ops.
    """
    from torch.onnx.symbolic_helper import _default_onnx_opset_version, _set_opset_version
    opset_version = opset_version or _default_onnx_opset_version
    _set_opset_version(opset_version)
    # operator_export_type is set to ONNX_FALLTHROUGH by default so that if an op is not supported
    # in ONNX, fall through will occur and export the operator as is, as a custom ONNX op.
    operator_export_type = OperatorExportTypes.ONNX_FALLTHROUGH
    with exporter_context(model, training):
        args = _decide_input_format(model, args)
        graph, params_dict, torch_out = _model_to_graph(
            model, args,
            # So that if an op connot be converted to ONNX, it will be kept
            # as-is rather than cause a failure.
            operator_export_type=OperatorExportTypes.ONNX_FALLTHROUGH)
    unsupported_ops = list()
    supported_namespaces = ("onnx", "prim")
    for node in graph.nodes():
        if node.kind().split(":")[0] not in supported_namespaces:
            unsupported_ops.append(node.kind())
    return graph, unsupported_ops
