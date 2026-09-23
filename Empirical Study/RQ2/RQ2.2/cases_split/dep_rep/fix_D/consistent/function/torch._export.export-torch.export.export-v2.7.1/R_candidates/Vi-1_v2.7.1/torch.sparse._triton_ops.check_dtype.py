def check_dtype(f_name, t, dtype, *additional_dtypes):
    check(
        t.dtype == dtype
        and t.dtype
        in ((torch.half, torch.bfloat16, torch.float) + tuple(*additional_dtypes)),
        f"{f_name}(): all inputs are expected to be of the same dtype "
        f"and one of (half, bfloat16, float32) or {additional_dtypes}, "
        f"but got dtype == {t.dtype}.",
    )
