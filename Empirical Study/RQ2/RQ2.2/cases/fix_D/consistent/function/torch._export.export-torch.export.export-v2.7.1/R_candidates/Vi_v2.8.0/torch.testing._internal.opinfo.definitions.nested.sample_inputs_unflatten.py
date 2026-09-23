def sample_inputs_unflatten(op_info, device, dtype, requires_grad, **kwargs):
    for sample_input in sample_inputs_unary_dimwise(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        # It will never make sense to operate on the ragged dim.
        # TODO: Handle this with error_inputs
        if sample_input.kwargs["dim"] == sample_input.input._ragged_idx:
            continue

        D = sample_input.input.size(sample_input.kwargs["dim"])
        # sizes should multiply to be D
        yield _update_sample(sample_input, {"sizes": [D, 1]})
        yield _update_sample(sample_input, {"sizes": [1, D]})
        if D % 2 == 0:
            yield _update_sample(sample_input, {"sizes": [D // 2, 2]})
            yield _update_sample(sample_input, {"sizes": [2, D // 2]})
