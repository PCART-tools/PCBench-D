def export_to_pretty_string(model, args, f, export_params=True, verbose=False, training=None,
                            input_names=None, output_names=None, operator_export_type=OperatorExportTypes.ONNX,
                            export_type=ExportTypes.PROTOBUF_FILE, example_outputs=None,
                            google_printer=False, opset_version=None, _retain_param_name=None,
                            keep_initializers_as_inputs=None, custom_opsets=None, add_node_names=True,
                            do_constant_folding=True, dynamic_axes=None):
    if f is not None:
        warnings.warn("'f' is deprecated and ignored. It will be removed in the next PyTorch release.")
    if _retain_param_name is not None:
        warnings.warn("'_retain_param_name' is deprecated and ignored. "
                      "It will be removed in the next PyTorch release.")
    return _export_to_pretty_string(model, args, f, export_params, verbose, training,
                                    input_names, output_names, operator_export_type,
                                    export_type, example_outputs, google_printer,
                                    opset_version, do_constant_folding=do_constant_folding,
                                    add_node_names=add_node_names,
                                    keep_initializers_as_inputs=keep_initializers_as_inputs,
                                    custom_opsets=custom_opsets, dynamic_axes=dynamic_axes)
