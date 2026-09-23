def _max_pool3d(
    input: Tensor, kernel_size: BroadcastingList3[int],
    stride: Optional[BroadcastingList3[int]] = None,
    padding: BroadcastingList3[int] = 0,
    dilation: BroadcastingList3[int] = 1,
    ceil_mode: bool = False,
    return_indices: bool = False
) -> Tensor:
    # See: https://github.com/pytorch/pytorch/pull/62544#issuecomment-896195121
    # and https://github.com/pytorch/pytorch/issues/62545 for context
    if ceil_mode != return_indices:
        warnings.warn("Note that order of the arguments: ceil_mode and return_indices will change"
                      "to match the args list in nn.MaxPool3d in a future release.")

    if has_torch_function_unary(input):
        return handle_torch_function(
            max_pool3d,
            (input,),
            input,
            kernel_size,
            stride=stride,
            padding=padding,
            dilation=dilation,
            ceil_mode=ceil_mode,
            return_indices=return_indices,
        )
    if stride is None:
        stride = torch.jit.annotate(List[int], [])
    return torch.max_pool3d(input, kernel_size, stride, padding, dilation, ceil_mode)
