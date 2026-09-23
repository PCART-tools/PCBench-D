def _low_memory_max_pool2d_with_offsets_aten(
    self,
    kernel_size,
    stride,
    padding,
    dilation,
    ceil_mode,
):
    vals, indices = torch.ops.aten.max_pool2d_with_indices(
        self, kernel_size, stride, padding, dilation, ceil_mode
    )

    input_width = self.shape[-1]
    kernel_width = kernel_size[1]

    bh_shape = [1] * self.ndim
    bh_shape[-2] = -1
    bh = torch.arange(indices.shape[-2], dtype=torch.int64, device=self.device).view(
        bh_shape
    )

    bw_shape = [1] * self.ndim
    bw_shape[-1] = -1
    bw = torch.arange(indices.shape[-1], dtype=torch.int64, device=self.device).view(
        bw_shape
    )

    hbase = bh * stride[0] - padding[0]
    wbase = bw * stride[1] - padding[1]

    ih = indices // input_width
    iw = indices - (ih * input_width)

    h_inc = ih - hbase
    w_inc = iw - wbase

    offsets = h_inc * kernel_width + w_inc

    return vals, offsets.to(torch.int8)
