def _is_fp(value):
    if value:
        if isinstance(value, torch.Tensor):
            return value.dtype in (torch.float16, torch.float32, torch.float64, torch.bfloat16)
        else:
            type = value.type().scalarType()
            if type is None:
                warnings.warn("Type cannot be inferred, which might cause exported graph to produce incorrect results.")
            return type in ("Float", "Double", "Half", "BFloat16")
    return False
