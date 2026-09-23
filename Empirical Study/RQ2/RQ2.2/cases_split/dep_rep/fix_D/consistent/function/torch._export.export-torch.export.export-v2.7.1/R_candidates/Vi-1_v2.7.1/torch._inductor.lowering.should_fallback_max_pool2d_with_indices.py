def should_fallback_max_pool2d_with_indices(kernel_size, dilation):
    kernel_size = pad_listlike(kernel_size, 2)
    window_size = kernel_size[0] * kernel_size[1]
    return (window_size > 25) or any(d > 1 for d in dilation)
