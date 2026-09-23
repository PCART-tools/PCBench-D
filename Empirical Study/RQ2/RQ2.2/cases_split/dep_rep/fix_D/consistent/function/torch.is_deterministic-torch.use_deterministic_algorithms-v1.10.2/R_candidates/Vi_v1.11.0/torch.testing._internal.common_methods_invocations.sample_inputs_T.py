def sample_inputs_T(self, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    shapes = ((), (M, M))
    return (SampleInput(make_arg(shape)) for shape in shapes)
