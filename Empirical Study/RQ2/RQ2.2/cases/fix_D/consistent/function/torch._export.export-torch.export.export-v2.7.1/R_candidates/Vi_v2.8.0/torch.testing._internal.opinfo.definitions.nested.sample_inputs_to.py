def sample_inputs_to(op_info, device, dtype, requires_grad, op_kwargs=None, **kwargs):
    for njt in _sample_njts(
        device=device,
        dtype=dtype,
        requires_grad=requires_grad,
        dims=[2, 3, 4],
    ):
        other_dtypes = (
            d for d in (torch.float32, torch.half, torch.double) if d is not dtype
        )
        for other_dtype in other_dtypes:
            sample_name = f"{njt.dim()}D: {dtype} -> {other_dtype}"
            yield SampleInput(_clone(njt), kwargs={"dtype": dtype}, name=sample_name)

        # only include device transfer for CUDA inputs
        if "cuda" in device:
            other_device = "cpu"
            sample_name = f"{_describe_njt(njt)}: {device} -> {other_device}"
            yield SampleInput(
                _clone(njt), kwargs={"device": other_device}, name=sample_name
            )
