def get_comparison_dtype(a, b):
    # TODO: update this when promote_types supports bfloat16 and/or
    # isclose supports bfloat16.
    a_dtype = torch.float32 if a.dtype is torch.bfloat16 else a.dtype
    b_dtype = torch.float32 if b.dtype is torch.bfloat16 else b.dtype

    compare_dtype = torch.promote_types(a_dtype, b_dtype)

    # non-CUDA (CPU, for example) float16 -> float32
    # TODO: update this when isclose is implemented for CPU float16
    if (compare_dtype is torch.float16 and
        (a.device != b.device or a.device.type != 'cuda' or
            b.device.type != 'cuda')):
        compare_dtype = torch.float32

    return compare_dtype
