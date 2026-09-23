@_format_argument.register
def _torch_tensor(obj: torch.Tensor) -> str:
    return f"Tensor({fx_type_utils.from_torch_dtype_to_abbr(obj.dtype)}{_stringify_shape(obj.shape)})"
