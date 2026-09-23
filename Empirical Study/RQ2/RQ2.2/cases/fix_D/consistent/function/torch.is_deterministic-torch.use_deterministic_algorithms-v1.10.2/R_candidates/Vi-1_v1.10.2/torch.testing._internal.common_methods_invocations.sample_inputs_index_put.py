def sample_inputs_index_put(op_info, device, dtype, requires_grad, **kwargs):
    inputs = []
    for accumulate in [False, True]:
        # Test with indices arg
        inputs.append(SampleInput(
            make_tensor((S, S,), device, dtype, low=None, high=None, requires_grad=requires_grad),
            args=(
                (index_variable(2, S, device=device), ),
                make_tensor((2, S), device, dtype, low=None, high=None)),
            kwargs=dict(accumulate=accumulate)))

        # Test with mask arg
        mask = torch.zeros(S, dtype=torch.bool) if accumulate else mask_not_all_zeros((S,))
        inputs.append(SampleInput(
            make_tensor((S, S), device, dtype, low=None, high=None, requires_grad=requires_grad),
            args=(
                (mask, ),
                make_tensor((S,), device, dtype, low=None, high=None),),
            kwargs=dict(accumulate=accumulate)))

    return inputs
