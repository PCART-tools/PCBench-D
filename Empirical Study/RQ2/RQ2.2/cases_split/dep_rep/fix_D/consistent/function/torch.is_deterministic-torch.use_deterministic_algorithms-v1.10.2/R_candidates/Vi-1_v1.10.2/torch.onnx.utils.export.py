def export(model, args, f, export_params=True, verbose=False, training=None,
           input_names=None, output_names=None, operator_export_type=None,
           opset_version=None, _retain_param_name=None, do_constant_folding=True,
           example_outputs=None, strip_doc_string=None, dynamic_axes=None,
           keep_initializers_as_inputs=None, custom_opsets=None,
           enable_onnx_checker=None, use_external_data_format=None):
    if operator_export_type is None:
        if torch.onnx.PYTORCH_ONNX_CAFFE2_BUNDLE:
            operator_export_type = OperatorExportTypes.ONNX_ATEN_FALLBACK
        else:
            operator_export_type = OperatorExportTypes.ONNX

    if enable_onnx_checker is not None:
        warnings.warn("'enable_onnx_checker' is deprecated and ignored. It will be removed in "
                      "the next PyTorch release. To proceed despite ONNX checker failures, "
                      "catch torch.onnx.ONNXCheckerError.")
    if _retain_param_name is not None:
        warnings.warn("'_retain_param_name' is deprecated and ignored. "
                      "It will be removed in the next PyTorch release.")
    if strip_doc_string is not None:
        warnings.warn("`strip_doc_string' is deprecated and ignored. Will be removed in "
                      "next PyTorch release. It's combined with `verbose' argument now. ")
    if example_outputs is not None:
        warnings.warn("`example_outputs' is deprecated and ignored. Will be removed in "
                      "next PyTorch release.")
    if use_external_data_format is not None:
        warnings.warn("`use_external_data_format' is deprecated and ignored. Will be removed in next "
                      "PyTorch release. The code will work as it is False if models are not larger than 2GB, "
                      "Otherwise set to False because of size limits imposed by Protocol Buffers.")

    _export(model, args, f, export_params, verbose, training, input_names, output_names,
            operator_export_type=operator_export_type, opset_version=opset_version,
            do_constant_folding=do_constant_folding, example_outputs=example_outputs,
            dynamic_axes=dynamic_axes, keep_initializers_as_inputs=keep_initializers_as_inputs,
            custom_opsets=custom_opsets, use_external_data_format=use_external_data_format)
