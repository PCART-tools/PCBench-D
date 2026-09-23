def filter_incompatible_and_dtype_convert_kwargs(kwargs):
    """Filter out kwargs that are not supported by onnxscript."""
    filtered = {}
    for key, value in kwargs.items():
        if key in {
            "layout",
            "device",
            "requires_grad",
            "pin_memory",
            "memory_format",
            "implicit",
        }:
            continue
        if key == "dtype":
            if value is None:
                # We omit if dtype is not provided, because onnxscript handles the
                # default case.
                continue
            else:
                value = int(jit_type_utils.JitScalarType.from_dtype(value).onnx_type())  # type: ignore[call-overload]
        filtered[key] = value
    return filtered
