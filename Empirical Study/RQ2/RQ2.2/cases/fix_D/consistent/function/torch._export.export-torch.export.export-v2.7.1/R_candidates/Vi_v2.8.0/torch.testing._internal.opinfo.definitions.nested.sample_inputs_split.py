def sample_inputs_split(op_info, device, dtype, requires_grad, **kwargs):
    for sample_input in sample_inputs_unary_dimwise(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        # ragged dim chunking: test a single split size
        if sample_input.kwargs["dim"] == sample_input.input._ragged_idx:
            yield _update_sample(sample_input, {"split_size_or_sections": 3})
        # other dim chunking: test different split sizes
        else:
            D = sample_input.input.size(sample_input.kwargs["dim"])
            for split_size in [1, D // 2, D - 1, D]:
                yield _update_sample(
                    sample_input, {"split_size_or_sections": split_size}
                )
