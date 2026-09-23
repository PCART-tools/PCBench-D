@register_lowering(prims._low_memory_max_pool2d_with_offsets, type_promotion_kind=None)
def _low_memory_max_pool2d_with_offsets(
    x,
    kernel_size,
    stride,
    padding,
    dilation,
    ceil_mode=False,
):
    # assert we are not on a fallback path, the inductor decomp should have guaranteed this
    kernel_size, stride, padding, dilation, _ = max_pool2d_checks(
        x,
        kernel_size,
        stride,
        padding,
        dilation,
        assert_fallback=False,
    )

    with config.patch(unroll_reductions_threshold=25):
        result, offsets = _max_pool2d_with_offsets(
            x,
            kernel_size,
            stride,
            padding,
            dilation,
            ceil_mode,
        )
        return result, to_dtype(offsets, torch.int8)
