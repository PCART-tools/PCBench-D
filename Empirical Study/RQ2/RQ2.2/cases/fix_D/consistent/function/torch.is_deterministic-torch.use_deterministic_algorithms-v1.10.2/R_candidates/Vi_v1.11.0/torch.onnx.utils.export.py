def export(model, args, f, export_params=True, verbose=False, training=None,
           input_names=None, output_names=None, operator_export_type=None,
           opset_version=None, do_constant_folding=True, dynamic_axes=None,
           keep_initializers_as_inputs=None, custom_opsets=None,
           export_modules_as_functions=False):
    if operator_export_type is None:
        if torch.onnx.PYTORCH_ONNX_CAFFE2_BUNDLE:
            operator_export_type = OperatorExportTypes.ONNX_ATEN_FALLBACK
        else:
            operator_export_type = OperatorExportTypes.ONNX

    _export(model, args, f, export_params, verbose, training, input_names, output_names,
            operator_export_type=operator_export_type, opset_version=opset_version,
            do_constant_folding=do_constant_folding, dynamic_axes=dynamic_axes,
            keep_initializers_as_inputs=keep_initializers_as_inputs,
            custom_opsets=custom_opsets, export_modules_as_functions=export_modules_as_functions)
