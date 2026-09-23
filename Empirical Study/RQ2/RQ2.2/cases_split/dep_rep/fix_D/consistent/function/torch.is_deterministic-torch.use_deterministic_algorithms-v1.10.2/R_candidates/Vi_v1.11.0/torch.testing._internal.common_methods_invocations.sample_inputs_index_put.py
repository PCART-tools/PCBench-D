def sample_inputs_index_put(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    inputs = []
    for accumulate in [False, True]:
        # Test with indices arg
        inputs.append(SampleInput(
            make_arg((S, S,)),
            args=((index_variable(2, S, device=device),), make_arg((2, S))),
            kwargs=dict(accumulate=accumulate)))

        # Test with mask arg
        mask = torch.zeros(S, dtype=torch.bool) if accumulate else mask_not_all_zeros((S,))
        inputs.append(SampleInput(
            make_arg((S, S)),
            args=((mask, ), make_arg((S,))),
            kwargs=dict(accumulate=accumulate)))

    return inputs
