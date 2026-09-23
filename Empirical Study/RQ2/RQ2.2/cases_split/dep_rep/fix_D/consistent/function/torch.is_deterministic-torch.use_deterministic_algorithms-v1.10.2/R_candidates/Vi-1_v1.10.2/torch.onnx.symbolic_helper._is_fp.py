def _is_fp(value):
    if value:
        if isinstance(value, torch.Tensor):
            type = value.dtype
            return (type == "torch.float32") or (type == "torch.float64") or (type == "torch.float16")
        else:
            type = value.type().scalarType()
            if type is None:
                warnings.warn("Type cannot be inferred, which might cause exported graph to produce incorrect results.")
            return (type == "Float") or (type == "Double") or (type == "Half")
    return False
