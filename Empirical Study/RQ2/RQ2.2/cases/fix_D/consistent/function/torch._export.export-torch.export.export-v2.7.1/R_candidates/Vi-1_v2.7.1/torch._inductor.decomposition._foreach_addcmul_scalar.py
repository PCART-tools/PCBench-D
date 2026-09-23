@register_decomposition(aten._foreach_addcmul.Scalar)
def _foreach_addcmul_scalar(
    self: list[torch.Tensor],
    left_tensors: list[torch.Tensor],
    right_tensors: list[torch.Tensor],
    scalar: float = 1,
) -> list[torch.Tensor]:
    return aten._foreach_add.List(
        self, aten._foreach_mul.List(left_tensors, right_tensors), alpha=scalar
    )
