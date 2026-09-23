@maybe_register_decomposition(aten.log_sigmoid_forward.default)
def log_sigmoid_forward(self: Tensor) -> tuple[Tensor, Tensor]:
    min = torch.minimum(self.new_zeros(()), self)
    z = torch.exp(-torch.abs(self))
    if self.is_cuda or self.is_xpu:
        buffer = self.new_zeros((0,))
    else:
        buffer = z
    return min - torch.log1p(z), buffer
