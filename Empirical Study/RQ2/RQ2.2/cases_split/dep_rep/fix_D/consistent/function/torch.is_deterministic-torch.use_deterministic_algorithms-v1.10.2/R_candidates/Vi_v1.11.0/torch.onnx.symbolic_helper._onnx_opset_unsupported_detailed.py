def _onnx_opset_unsupported_detailed(op_name, current_opset, supported_opset, reason):
    raise RuntimeError("Unsupported: ONNX export of {} in "
                       "opset {}. {}. Please try opset version {}.".format(op_name, current_opset, reason, supported_opset))
