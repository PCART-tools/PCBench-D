def _low_memory_max_pool2d_offsets_to_indices_aten(
    offsets, kernel_width, input_width, stride, padding
):
    offsets = offsets.to(torch.int64)
    h_inc = offsets // kernel_width
    w_inc = offsets - (h_inc * kernel_width)

    bh_shape = [1] * offsets.ndim
    bh_shape[-2] = -1
    bh = torch.arange(offsets.shape[-2], dtype=torch.int64, device=offsets.device).view(
        bh_shape
    )

    bw_shape = [1] * offsets.ndim
    bw_shape[-1] = -1
    bw = torch.arange(offsets.shape[-1], dtype=torch.int64, device=offsets.device).view(
        bw_shape
    )

    hbase = bh * stride[0] - padding[0]
    wbase = bw * stride[1] - padding[1]

    ih = hbase + h_inc
    iw = wbase + w_inc
    return ih * input_width + iw
