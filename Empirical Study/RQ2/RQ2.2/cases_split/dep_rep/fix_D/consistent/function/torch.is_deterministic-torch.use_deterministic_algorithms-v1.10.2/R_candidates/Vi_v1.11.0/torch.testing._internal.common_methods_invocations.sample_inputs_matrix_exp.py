def sample_inputs_matrix_exp(op_info, device, dtype, requires_grad, **kwargs):
    samples = (
        SampleInput(make_tensor((S, S), device, dtype, requires_grad=requires_grad)),
        SampleInput(make_tensor((S, S, S), device, dtype, requires_grad=requires_grad)),
    )

    return samples
