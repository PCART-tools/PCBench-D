def max_pool2d_checks(
    x, kernel_size, stride, padding, dilation, *, assert_fallback=None
):
    if padding == 0:
        padding = [0, 0]
    if dilation == 1:
        dilation = [1, 1]
    if not stride:
        stride = kernel_size

    kernel_size = pad_listlike(kernel_size, 2)
    stride = pad_listlike(stride, 2)
    padding = pad_listlike(padding, 2)
    dilation = pad_listlike(dilation, 2)

    assert isinstance(x, TensorBox)
    assert len(kernel_size) == 2
    assert len(stride) == 2
    assert len(padding) == 2
    assert len(dilation) == 2
    assert len(x.get_size()) in (3, 4)

    use_fallback = should_fallback_max_pool2d_with_indices(kernel_size, dilation)
    if assert_fallback is not None:
        assert use_fallback == assert_fallback

    return kernel_size, stride, padding, dilation, use_fallback
