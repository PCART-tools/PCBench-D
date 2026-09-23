def may_require_grad(dtype):
    return dtype.is_floating_point or dtype.is_complex
