def sample_inputs_prod(op_info, device, dtype, requires_grad):
    def make_arg(shape):
        # shrink values to be in the interval [-1, +1] for better precision in gradgradcheck
        return make_tensor(shape, device, dtype, low=-1, high=+1, requires_grad=requires_grad)

    def prod_single_zero():
        result = make_arg(2 * (S,))
        with torch.no_grad():
            result[0, 1] = 0
        return result

    # will not be needed once OpInfo tests support Iterables
    def sample_generator():
        for sample in sample_inputs_cumprod(op_info, device, dtype, requires_grad):
            yield SampleInput(sample.input)  # only Tensor, ignore other inputs
            yield sample
            sample.kwargs['keepdim'] = True
            yield sample
        yield SampleInput(prod_single_zero())
        yield SampleInput(make_arg((3, 3, 3)), args=(1,))
        yield SampleInput(make_arg((3, 3, 3)), args=(1,), kwargs={'keepdim': True})

        # test zero scalar tensor
        zero = make_arg(())
        with torch.no_grad():
            zero.zero_()
        yield SampleInput(zero)
        yield SampleInput(zero, args=(0,))
        yield SampleInput(zero, args=(0,), kwargs={'keepdim': True})

    return list(sample_generator())
