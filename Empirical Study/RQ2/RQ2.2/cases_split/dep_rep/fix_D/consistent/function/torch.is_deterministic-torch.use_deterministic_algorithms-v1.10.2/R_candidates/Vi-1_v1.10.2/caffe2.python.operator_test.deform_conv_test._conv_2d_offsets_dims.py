def _conv_2d_offsets_dims(
    batch_size,
    size,
    kernel,
    pad_h,
    pad_w,
    dilation,
    stride_h,
    stride_w,
    deformable_group,
):
    dims = [batch_size, 2 * kernel * kernel * deformable_group]
    dims.extend(
        _conv_2d_output_size(size, kernel, pad_h, pad_w, dilation, stride_h, stride_w)
    )
    return dims
