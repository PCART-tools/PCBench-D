def _dequantize_tensor_list(t: Any) -> Any:
    return (
        list(_dequantize_tensor_list(x) for x in t)
        if type(t) is list
        else t.dequantize()
        if t.is_quantized
        else t
    )
