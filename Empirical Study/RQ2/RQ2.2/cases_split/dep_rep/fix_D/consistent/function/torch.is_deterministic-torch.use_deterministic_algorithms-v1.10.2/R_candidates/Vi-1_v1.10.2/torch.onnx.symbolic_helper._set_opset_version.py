def _set_opset_version(opset_version):
    global _export_onnx_opset_version
    if opset_version == _default_onnx_opset_version:
        _export_onnx_opset_version = opset_version
        return
    if opset_version in _onnx_stable_opsets + [_onnx_main_opset]:
        _export_onnx_opset_version = opset_version
        return
    raise ValueError("Unsupported ONNX opset version: " + str(opset_version))
