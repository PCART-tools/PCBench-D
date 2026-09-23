@_format_argument.register
def _onnxscript_torch_script_tensor(obj: graph_building.TorchScriptTensor) -> str:
    return f"`TorchScriptTensor({fx_type_utils.from_torch_dtype_to_abbr(obj.dtype)}{_stringify_shape(obj.shape)})`"  # type: ignore[arg-type]  # noqa: B950
