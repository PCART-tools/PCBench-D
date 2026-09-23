def sample_inputs_mm(op_info, device, dtype, requires_grad, **kwargs):
    first_shape, second_shape = (S, M), (M, S)
    sample_inputs = []
    sample_inputs.append(
        SampleInput(make_tensor(first_shape, device, dtype,
                                requires_grad=requires_grad),
                    args=(make_tensor(second_shape, device, dtype,
                                      requires_grad=requires_grad),)))

    if dtype.is_complex:
        sample_inputs.append(
            SampleInput(make_tensor(first_shape, device, dtype,
                                    requires_grad=requires_grad),
                        args=(
                            make_tensor(second_shape, device, dtype,
                                        requires_grad=requires_grad).conj(),)))

        sample_inputs.append(
            SampleInput(make_tensor(first_shape, device, dtype,
                                    requires_grad=requires_grad).transpose(0, 1),
                        args=(
                            make_tensor(second_shape, device, dtype,
                                        requires_grad=requires_grad).transpose(0, 1).conj(),)))
    return sample_inputs
