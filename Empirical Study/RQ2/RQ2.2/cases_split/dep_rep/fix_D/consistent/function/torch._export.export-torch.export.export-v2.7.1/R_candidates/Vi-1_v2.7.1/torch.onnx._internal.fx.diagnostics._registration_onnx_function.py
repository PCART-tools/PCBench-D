@_format_argument.register
def _registration_onnx_function(obj: registration.ONNXFunction) -> str:
    # TODO: Compact display of `param_schema`.
    return f"registration.ONNXFunction({obj.op_full_name}, is_custom={obj.is_custom}, is_complex={obj.is_complex})"
