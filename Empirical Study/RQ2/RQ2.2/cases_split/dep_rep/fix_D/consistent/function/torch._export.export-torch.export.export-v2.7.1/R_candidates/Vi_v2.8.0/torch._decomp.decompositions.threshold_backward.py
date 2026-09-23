@register_decomposition(aten.threshold_backward)
@out_wrapper("grad_input")
def threshold_backward(grad_output: Tensor, self: Tensor, threshold: float):
    return torch.where(self <= threshold, 0, grad_output)
