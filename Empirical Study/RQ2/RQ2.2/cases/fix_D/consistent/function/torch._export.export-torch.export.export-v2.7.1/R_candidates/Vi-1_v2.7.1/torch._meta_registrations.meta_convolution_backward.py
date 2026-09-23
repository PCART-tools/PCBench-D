@register_meta([aten.convolution_backward.default])
def meta_convolution_backward(
    grad_output_,
    input_,
    weight_,
    bias_sizes_opt,
    stride,
    padding,
    dilation,
    transposed,
    output_padding,
    groups,
    output_mask,
):
    # High level logic taken from slow_conv3d_backward_cpu which should
    # be representative of all convolution_backward impls
    backend_grad_input = None
    backend_grad_weight = None
    backend_grad_bias = None

    if output_mask[0]:
        backend_grad_input = grad_output_.new_empty(input_.size())
    if output_mask[1]:
        backend_grad_weight = grad_output_.new_empty(weight_.size())
    if output_mask[2]:
        backend_grad_bias = grad_output_.new_empty(bias_sizes_opt)

    return (backend_grad_input, backend_grad_weight, backend_grad_bias)
