    @register_meta(torch.ops.quantized.max_pool2d)
    def meta_quantized_max_pool2d(
        input,
        kernel_size,
        stride=(),
        padding=(0,),
        dilation=(1,),
        ceil_mode=False,
    ):
        (
            nInputPlane,
            outputHeight,
            outputWidth,
        ) = max_pool2d_checks_and_compute_shape(
            input, kernel_size, stride, padding, dilation, ceil_mode
        )
        nbatch = input.size(-4) if input.dim() == 4 else 1
        memory_format = torch.channels_last
        if input.dim() == 3:
            size = [nInputPlane, outputHeight, outputWidth]
        else:
            size = [nbatch, nInputPlane, outputHeight, outputWidth]
        return torch.empty(
            size,
            dtype=input.dtype,
            device=input.device,
            memory_format=memory_format,
        )
