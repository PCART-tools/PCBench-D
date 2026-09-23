@register_function_func(NATIVE_REDUCE_FNS + TORCH_REDUCE_FNS + TENSOR_REDUCE_FNS)
def _general_function_reductions(func, *args, **kwargs):
    return _apply_reduction(func, *args, **kwargs)
