def rand_strided(
    size: Sequence[int],
    stride: Sequence[int],
    dtype: torch.dtype = torch.float32,
    device: Union[str, torch.device] = "cpu",
    extra_size: int = 0,
) -> torch.Tensor:
    needed_size = (
        sum((shape - 1) * stride for shape, stride in zip(size, stride))
        + 1
        + extra_size
    )
    if dtype.is_floating_point:
        if dtype.itemsize == 1:
            """
            normal distribution kernel is not implemented for fp8..
            Workaround that by creating a fp16 tensor and then cast.
            """
            buffer = torch.randn(needed_size, dtype=torch.float16, device=device).to(
                dtype=dtype
            )
        else:
            buffer = torch.randn(needed_size, dtype=dtype, device=device)
    else:
        buffer = torch.zeros(size=[needed_size], dtype=dtype, device=device)
    return torch.as_strided(buffer, size, stride)
