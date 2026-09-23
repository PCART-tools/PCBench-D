@register_decomposition([aten.view_copy.dtype])
def view_copy_dtype(
    self: torch.Tensor,
    dtype: torch.dtype,
) -> torch.Tensor:
    return self.to(dtype).clone()
