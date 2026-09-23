def sample_inputs_index_put(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    for accumulate in [False, True]:
        # Test with indices arg
        yield SampleInput(
            make_arg((S, S,)),
            # As defined in the docs, if accumulate is false, duplicate indices are not supported
            (index_variable(2 if accumulate else 1, S, device=device),),
            make_arg((2 if accumulate else 1, S)),
            accumulate=accumulate)

        # Test with mask arg
        mask = torch.zeros(S, dtype=torch.bool) if accumulate else mask_not_all_zeros((S,))
        yield SampleInput(
            make_arg((S, S)), (mask, ), make_arg((S,)), accumulate=accumulate)
