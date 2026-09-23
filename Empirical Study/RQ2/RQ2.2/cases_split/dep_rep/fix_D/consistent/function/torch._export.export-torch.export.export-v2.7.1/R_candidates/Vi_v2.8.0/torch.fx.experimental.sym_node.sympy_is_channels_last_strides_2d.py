def sympy_is_channels_last_strides_2d(sizes, strides):
    return sympy_is_channels_last_strides_generic(sizes, strides, [1, 3, 2, 0])
