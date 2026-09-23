@_format_argument.register
def _onnxscript_traced_onnx_function(obj: onnxscript.TracedOnnxFunction) -> str:
    return f"`TracedOnnxFunction({obj.name})`"
