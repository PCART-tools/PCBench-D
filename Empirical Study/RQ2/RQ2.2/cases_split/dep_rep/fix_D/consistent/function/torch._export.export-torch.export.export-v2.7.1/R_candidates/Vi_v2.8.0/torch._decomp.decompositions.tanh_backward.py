@register_decomposition(aten.tanh_backward)
@out_wrapper("grad_input")
@pw_cast_for_opmath
def tanh_backward(out_grad: Tensor, y: Tensor):
    return out_grad * (1 - y * y).conj_physical()
