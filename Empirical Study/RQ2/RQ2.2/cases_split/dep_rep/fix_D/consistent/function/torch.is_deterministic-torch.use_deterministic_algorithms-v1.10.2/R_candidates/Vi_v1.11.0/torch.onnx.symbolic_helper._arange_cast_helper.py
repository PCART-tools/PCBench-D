def _arange_cast_helper(g, end, start=None, step=None, dtype=None):
    def _is_all_integral(scalars):
        for scalar in scalars:
            try:
                if scalar.type().scalarType() != "Long":
                    return False
            except Exception:
                pass
        return True

    # This logic is based on torch.arange docs. If "dtype" is provided,
    # infer input types from dtype. If not, then check if any of start, stop,
    # or step are floating point, and infer the type from get_default.
    # Otherwise, the dtype is inferred to be torch.int64.
    if dtype is None or (_is_value(dtype) and _is_none(dtype)):
        if _is_all_integral([start, end, step]):
            type = scalar_type_to_pytorch_type.index(torch.int64)
        else:
            type = scalar_type_to_pytorch_type.index(torch.get_default_dtype())
    else:
        type = dtype

    start = g.op("Cast", start, to_i=scalar_type_to_onnx[type]) if start else None
    end = g.op("Cast", end, to_i=scalar_type_to_onnx[type]) if end else None
    step = g.op("Cast", step, to_i=scalar_type_to_onnx[type]) if step else None
    return type, end, start, step
