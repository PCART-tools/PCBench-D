def sample_inputs_diag(op_info, device, dtype, requires_grad, **kwargs):
    vec_sample = SampleInput(make_tensor((M, ), device, dtype, low=None, high=None, requires_grad=requires_grad))

    tensors = (
        make_tensor((M, M), device, dtype, low=None, high=None, requires_grad=requires_grad),
        make_tensor((3, 5), device, dtype, low=None, high=None, requires_grad=requires_grad),
        make_tensor((5, 3), device, dtype, low=None, high=None, requires_grad=requires_grad),
    )

    args = ((), (2,), (-2,), (1,), (2,))

    samples = []
    for tensor, arg in product(tensors, args):
        samples.append(SampleInput(tensor, args=arg))

    return samples + [vec_sample]
