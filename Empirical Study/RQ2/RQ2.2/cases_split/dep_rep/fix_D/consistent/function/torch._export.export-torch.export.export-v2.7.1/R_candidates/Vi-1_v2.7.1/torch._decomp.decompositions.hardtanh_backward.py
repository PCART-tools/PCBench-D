@register_decomposition(aten.hardtanh_backward)
@out_wrapper("grad_input")
def hardtanh_backward(
    grad_output: Tensor, self: Tensor, min_val: float, max_val: float
):
    return torch.where((self <= min_val) | (self >= max_val), 0.0, grad_output)
