@register_flop_formula([aten.convolution, aten._convolution])
def conv_flop(x_shape, w_shape, _bias, _stride, _padding, _dilation, transposed, *args, out_shape=None, **kwargs) -> int:
    """Count flops for convolution."""
    return conv_flop_count(x_shape, w_shape, out_shape, transposed=transposed)
