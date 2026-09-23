def _is_conv_transpose_fn(conv_fn: Callable):
    return conv_fn in [F.conv_transpose1d, F.conv_transpose2d]
