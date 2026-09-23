@_format_argument.register
def _onnxscript_onnx_function(obj: onnxscript.OnnxFunction) -> str:
    return f"`OnnxFunction({obj.name})`"
