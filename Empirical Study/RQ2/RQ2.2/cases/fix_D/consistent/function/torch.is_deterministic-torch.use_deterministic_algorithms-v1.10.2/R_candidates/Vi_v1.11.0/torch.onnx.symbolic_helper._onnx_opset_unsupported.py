def _onnx_opset_unsupported(op_name, current_opset, supported_opset):
    raise RuntimeError("Unsupported: ONNX export of {} in "
                       "opset {}. Please try opset version {}.".format(op_name, current_opset, supported_opset))
