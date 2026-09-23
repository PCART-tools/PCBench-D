@register_decomposition(aten.sigmoid_backward)
@out_wrapper("grad_input")
@pw_cast_for_opmath
def sigmoid_backward(out_grad: Tensor, y: Tensor):
    return out_grad * (y * (1 - y)).conj_physical()
