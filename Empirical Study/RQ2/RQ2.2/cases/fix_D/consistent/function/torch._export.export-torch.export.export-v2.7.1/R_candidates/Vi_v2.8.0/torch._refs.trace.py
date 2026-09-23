@register_decomposition(aten.trace)
@out_wrapper()
def trace(self: TensorLikeType) -> TensorLikeType:
    torch._check(
        self.ndim == 2, lambda: "expected a matrix, but got tensor with dim {self.ndim}"
    )
    return torch.sum(torch.diag(self, 0))
