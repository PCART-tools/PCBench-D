def error_inputs_t(op_info, device, **kwargs):
    yield ErrorInput(
        SampleInput(torch.randn(2, 3, 4, 5, device=device)),
        error_regex="expects a tensor with <= 2",
    )
