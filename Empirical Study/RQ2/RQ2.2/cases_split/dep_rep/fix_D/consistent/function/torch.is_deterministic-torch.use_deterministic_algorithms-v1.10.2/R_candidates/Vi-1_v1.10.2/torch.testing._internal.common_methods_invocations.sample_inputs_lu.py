def sample_inputs_lu(op_info, device, dtype, requires_grad=False, **kwargs):
    # not needed once OpInfo tests support Iterables
    def generate_samples():
        batch_shapes = ((), (3,), (3, 3))
        for batch_shape, get_infos, size_delta in product(batch_shapes, (True, False), (-2, -1, 0, +1, +2)):
            shape = batch_shape + (S + size_delta, S)
            input = make_tensor(shape, device, dtype, requires_grad=requires_grad, low=None, high=None)
            yield SampleInput(input, args=(True, get_infos))

    return list(generate_samples())
