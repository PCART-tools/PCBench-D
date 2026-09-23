def export_to_pretty_string(model, args, export_params=True, verbose=False, training=None,
                            input_names=None, output_names=None, operator_export_type=OperatorExportTypes.ONNX,
                            export_type=ExportTypes.PROTOBUF_FILE, google_printer=False, opset_version=None,
                            keep_initializers_as_inputs=None, custom_opsets=None, add_node_names=True,
                            do_constant_folding=True, dynamic_axes=None):
    from torch.onnx.symbolic_helper import _default_onnx_opset_version, _set_opset_version
    from torch.onnx.symbolic_helper import _set_operator_export_type
    if opset_version is None:
        opset_version = _default_onnx_opset_version
    if custom_opsets is None:
        custom_opsets = {}
    _set_opset_version(opset_version)
    _set_operator_export_type(operator_export_type)
    from torch.onnx.symbolic_helper import _set_onnx_shape_inference
    _set_onnx_shape_inference(True)
    with exporter_context(model, training):
        val_keep_init_as_ip = _decide_keep_init_as_input(keep_initializers_as_inputs,
                                                         operator_export_type,
                                                         opset_version)
        val_add_node_names = _decide_add_node_names(add_node_names, operator_export_type)
        val_do_constant_folding = _decide_constant_folding(do_constant_folding, operator_export_type, training)
        args = _decide_input_format(model, args)
        graph, params_dict, torch_out = _model_to_graph(model, args, verbose, input_names,
                                                        output_names, operator_export_type,
                                                        val_do_constant_folding,
                                                        training=training, dynamic_axes=dynamic_axes)

        return graph._pretty_print_onnx(params_dict, opset_version, False,
                                        operator_export_type, google_printer,
                                        val_keep_init_as_ip, custom_opsets, val_add_node_names)
