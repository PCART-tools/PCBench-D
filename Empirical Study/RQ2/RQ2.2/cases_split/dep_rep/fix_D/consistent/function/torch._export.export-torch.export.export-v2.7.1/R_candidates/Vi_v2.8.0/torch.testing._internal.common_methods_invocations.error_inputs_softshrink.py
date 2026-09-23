def error_inputs_softshrink(op, device, **kwargs):
    yield ErrorInput(SampleInput(make_tensor((1,), dtype=torch.float, device=device), kwargs={"lambd": -0.5}),
                     error_regex="lambda must be greater or equal to 0, but found to be -0.5")
