def sample_inputs_split_with_sizes(op_info, device, dtype, requires_grad, **kwargs):
    for sample_input in sample_inputs_unary_dimwise(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        # It will never make sense to operate on the ragged dim.
        # TODO: Handle this with error_inputs
        if sample_input.kwargs["dim"] == sample_input.input._ragged_idx:
            continue

        D = sample_input.input.size(sample_input.kwargs["dim"])
        # splits should add up to D
        split1 = torch.randint(0, D - 1, size=()).item()
        split2 = D - split1
        yield _update_sample(sample_input, {"split_sizes": [split1, split2]})
