def bilinear(input1: Tensor, input2: Tensor, weight: Tensor, bias: Optional[Tensor] = None) -> Tensor:
    r"""
    Applies a bilinear transformation to the incoming data:
    :math:`y = x_1^T A x_2 + b`

    Shape:

        - input1: :math:`(N, *, H_{in1})` where :math:`H_{in1}=\text{in1\_features}`
          and :math:`*` means any number of additional dimensions.
          All but the last dimension of the inputs should be the same.
        - input2: :math:`(N, *, H_{in2})` where :math:`H_{in2}=\text{in2\_features}`
        - weight: :math:`(\text{out\_features}, \text{in1\_features},
          \text{in2\_features})`
        - bias: :math:`(\text{out\_features})`
        - output: :math:`(N, *, H_{out})` where :math:`H_{out}=\text{out\_features}`
          and all but the last dimension are the same shape as the input.
    """
    if has_torch_function_variadic(input1, input2, weight, bias):
        return handle_torch_function(
            bilinear,
            (input1, input2, weight, bias),
            input1, input2, weight,
            bias=bias
        )
    return torch.bilinear(input1, input2, weight, bias)
