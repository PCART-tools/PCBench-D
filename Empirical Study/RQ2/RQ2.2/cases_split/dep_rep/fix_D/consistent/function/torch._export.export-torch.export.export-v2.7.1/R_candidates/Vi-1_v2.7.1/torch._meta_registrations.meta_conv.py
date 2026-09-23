@register_meta(aten.convolution.default)
def meta_conv(
    input_tensor: torch.Tensor,
    weight: torch.Tensor,
    bias: torch.Tensor,
    stride: list[int],
    padding: list[int],
    dilation: list[int],
    is_transposed: bool,
    output_padding: list[int],
    groups: int,
):
    def pick_memory_format():
        if device_hint(input_tensor) == "cuda":
            if is_channels_last(input_tensor) or is_channels_last(weight):
                return torch.channels_last
        else:
            if is_channels_last(input_tensor):
                return torch.channels_last
        if input_tensor.is_contiguous(memory_format=torch.contiguous_format):
            return torch.contiguous_format
        elif input_tensor.is_contiguous(memory_format=torch.preserve_format):
            return torch.preserve_format

    shape_out = calc_conv_nd_return_shape(
        input_tensor,
        weight,
        stride,
        padding,
        dilation,
        is_transposed,
        groups,
        output_padding if is_transposed else None,
    )

    input_channels_dim = 1
    output_channels_dim = 1
    if input_tensor.size(input_channels_dim) == 0:
        shape_out[output_channels_dim] = 0

    out = input_tensor.new_empty(shape_out)
    out = out.to(memory_format=pick_memory_format())  # type: ignore[call-overload]
    return out
