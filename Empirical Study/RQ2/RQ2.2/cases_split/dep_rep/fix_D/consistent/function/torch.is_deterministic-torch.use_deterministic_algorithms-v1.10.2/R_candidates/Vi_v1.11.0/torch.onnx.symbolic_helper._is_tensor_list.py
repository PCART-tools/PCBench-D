def _is_tensor_list(x):
    return _is_list(x) and isinstance(x.type().getElementType(), torch._C.TensorType)
