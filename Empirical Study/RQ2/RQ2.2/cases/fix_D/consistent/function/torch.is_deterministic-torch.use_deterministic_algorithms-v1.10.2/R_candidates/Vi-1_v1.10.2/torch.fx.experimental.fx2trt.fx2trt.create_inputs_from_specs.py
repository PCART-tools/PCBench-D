def create_inputs_from_specs(input_specs):
    inputs = []

    for shape, dtype, device, shape_ranges, has_batch_dim in input_specs:
        if len(get_dynamic_dims(shape)):
            shape = shape_ranges[0][1]
        elif not has_batch_dim:
            shape = (1,) + tuple(shape)

        inputs.append(torch.randn(shape).to(dtype=dtype, device=device))

    return inputs
