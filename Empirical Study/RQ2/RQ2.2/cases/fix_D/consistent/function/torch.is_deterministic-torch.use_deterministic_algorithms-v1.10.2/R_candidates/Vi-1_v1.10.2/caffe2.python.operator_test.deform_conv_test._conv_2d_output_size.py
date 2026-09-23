def _conv_2d_output_size(size, kernel, pad_h, pad_w, dilation, stride_h, stride_w):
    return [
        _conv_1d_output_size(size, kernel, pad_h, dilation, stride_h),
        _conv_1d_output_size(size, kernel, pad_w, dilation, stride_w),
    ]
