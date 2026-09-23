def _find_missing_ops_onnx_export(model, args, f, verbose=False, training=TrainingMode.EVAL,
                                  input_names=None, output_names=None, opset_version=None, dynamic_axes=None):
    r"""
    This diagnostic tool runs your model with operator_export_type set to
    OperatorExportTypes.ONNX_FALLTHROUGH once in order to get a list of
    all the ops that are not supported/implemented by the current exporter

    operator_export_type is set to OperatorExportTypes.ONNX_FALLTHROUGH by default
        OperatorExportTypes.ONNX_FALLTHROUGH: If an op is not supported
        in ONNX, fall through and export the operator as is, as a custom
        ONNX op. Using this mode, the op can be exported and implemented by
        the user for their runtime backend.
        Example graph::

            graph(%0 : Float(2, 3, 4, strides=[12, 4, 1], requires_grad=0, device=cpu)):
                %6 : Long(requires_grad=0, device=cpu) = prim::Constant[value={0}]()
                %4 : None = prim::Constant()
                %5 : Float(2, 3, 4, strides=[12, 4, 1], requires_grad=0, device=cpu) = aten::cumsum(%0, %6, %4) # main.py:6:0
                return (%5)

        is exported as::

            graph(%0 : Float(2, 3, 4, strides=[12, 4, 1], requires_grad=0, device=cpu)):
                %6 : Long(requires_grad=0, device=cpu) = prim::Constant[value={0}]()
                %4 : None = prim::Constant()
                %5 : Float(2, 3, 4, strides=[12, 4, 1], requires_grad=0, device=cpu) = aten::cumsum(%0, %6, %4) # main.py:6:0
                return (%5)

        In the above example, aten::cumsum in not implemented in opset 9, hence exporter falls
        through and provides a list of unsupported ops, the result being:
            Unsupported ops : [aten:cumsum]
    """
    from torch.onnx.symbolic_helper import _default_onnx_opset_version, _set_opset_version
    if opset_version is None:
        opset_version = _default_onnx_opset_version
    _set_opset_version(opset_version)
    # operator_export_type is set ro ONNX_FALLTHROUGH by default so that if an op is not supported
    # in ONNX, fall through will occur and export the operator as is, as a custom ONNX op.
    operator_export_type = OperatorExportTypes.ONNX_FALLTHROUGH
    with select_model_mode_for_export(model, training):
        args = _decide_input_format(model, args)
        graph, params_dict, torch_out = _model_to_graph(model, args, verbose, input_names,
                                                        output_names, operator_export_type)
    # The output "unsupported_ops" will contain the names of all the ops that are not supported in ONNX
    unsupported_ops = list()
    for node in graph.nodes():
        if node.kind().split(":")[0] not in ["onnx", "prim"]:
            unsupported_ops.append(node.kind())
    return graph, unsupported_ops
