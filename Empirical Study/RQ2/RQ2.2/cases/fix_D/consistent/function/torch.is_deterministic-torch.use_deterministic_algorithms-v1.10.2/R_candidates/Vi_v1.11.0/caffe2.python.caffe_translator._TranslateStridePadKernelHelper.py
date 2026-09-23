def _TranslateStridePadKernelHelper(param, caffe_op):
    try:
        if (len(param.stride) > 1 or len(param.kernel_size) > 1 or
                len(param.pad) > 1):
            raise NotImplementedError(
                "Translator currently does not support non-conventional "
                "pad/kernel/stride settings."
            )
        stride = param.stride[0] if len(param.stride) else 1
        pad = param.pad[0] if len(param.pad) else 0
        kernel = param.kernel_size[0] if len(param.kernel_size) else 0
    except TypeError:
        # This catches the case of a PoolingParameter, in which case we are
        # having non-repeating pad, stride and kernel.
        stride = param.stride
        pad = param.pad
        kernel = param.kernel_size
    # Get stride
    if param.HasField("stride_h") or param.HasField("stride_w"):
        AddArgument(caffe_op, "stride_h", param.stride_h)
        AddArgument(caffe_op, "stride_w", param.stride_w)
    else:
        AddArgument(caffe_op, "stride", stride)
    # Get pad
    if param.HasField("pad_h") or param.HasField("pad_w"):
        if param.pad_h == param.pad_w:
            AddArgument(caffe_op, "pad", param.pad_h)
        else:
            AddArgument(caffe_op, "pad_t", param.pad_h)
            AddArgument(caffe_op, "pad_b", param.pad_h)
            AddArgument(caffe_op, "pad_l", param.pad_w)
            AddArgument(caffe_op, "pad_r", param.pad_w)
    else:
        AddArgument(caffe_op, "pad", pad)
    # Get kernel
    if param.HasField("kernel_h") or param.HasField("kernel_w"):
        AddArgument(caffe_op, "kernel_h", param.kernel_h)
        AddArgument(caffe_op, "kernel_w", param.kernel_w)
    else:
        AddArgument(caffe_op, "kernel", kernel)
