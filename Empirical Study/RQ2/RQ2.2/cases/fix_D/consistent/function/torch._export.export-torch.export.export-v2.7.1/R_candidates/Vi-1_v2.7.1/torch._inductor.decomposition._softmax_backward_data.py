@register_decomposition(aten._softmax_backward_data.default)
@pw_cast_for_opmath
def _softmax_backward_data(
    grad_output: torch.Tensor,
    output: torch.Tensor,
    dim: int,
    input_dtype: torch.dtype,
) -> torch.Tensor:
    new_grad_output = grad_output * output
    sum_new_grad = torch.sum(new_grad_output, dim=dim, keepdim=True)
    # grad_input = new_grad_output - output * sum_new_grad
    grad_input = inductor_prims.fma(-output, sum_new_grad, new_grad_output)

    # CPU kernel doesn't respect input_dtype, but following check doesn't work for meta tensor
    # if grad_output.device == torch.device("cpu"):
    #     return grad_input.contiguous()

    if grad_output.dtype != input_dtype:
        grad_input = grad_input.to(input_dtype)
    return grad_input.contiguous()
