def sample_inputs_masked_select(
    op_info, device, dtype, requires_grad, op_kwargs=None, **kwargs
):
    for njt in _sample_njts(
        device=device, dtype=dtype, requires_grad=requires_grad, dims=[2]
    ):
        yield SampleInput(
            njt,
            kwargs={"mask": (torch.randn_like(njt, requires_grad=False) < 0.0)},
            name=_describe_njt(njt),
        )
