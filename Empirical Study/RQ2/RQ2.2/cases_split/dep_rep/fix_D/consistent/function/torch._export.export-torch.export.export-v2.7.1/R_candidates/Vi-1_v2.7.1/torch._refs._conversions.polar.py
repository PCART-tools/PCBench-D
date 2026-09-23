@register_decomposition(torch._ops.ops.aten.polar)
# Note: polar has type promotion tests disabled due to different semantics.
# exact_dtype is for compat with complex_check_dtype from core.
@out_wrapper(exact_dtype=True)
def polar(abs: TensorLikeType, angle: TensorLikeType) -> TensorLikeType:
    result = torch.complex(abs, angle)
    result.real = abs * torch.cos(angle)
    result.imag = abs * torch.sin(angle)
    return result
