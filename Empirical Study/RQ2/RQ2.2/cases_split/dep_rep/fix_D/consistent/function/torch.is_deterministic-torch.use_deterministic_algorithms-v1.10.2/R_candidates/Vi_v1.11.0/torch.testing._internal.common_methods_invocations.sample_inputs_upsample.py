def sample_inputs_upsample(mode, self, device, dtype, requires_grad, **kwargs):
    N, C = 2, 3
    D = 4
    S = 3
    L = 5

    ranks_for_mode = {
        'nearest': [1, 2, 3],
        'bilinear': [2],
    }

    def shape(size, rank, with_batch_channel=True):
        if with_batch_channel:
            return tuple([N, C] + ([size] * rank))
        return tuple([size] * rank)

    make_arg = partial(make_tensor, device=device, dtype=dtype,
                       requires_grad=requires_grad, low=-1, high=1)

    sample_inputs = []
    for rank in ranks_for_mode[mode]:
        sample_inputs.extend([
            SampleInput(make_arg(shape(D, rank)),
                        kwargs=dict(size=shape(S, rank, False))),
            SampleInput(make_arg(shape(D, rank)),
                        kwargs=dict(size=shape(L, rank, False))),
            SampleInput(make_arg(shape(D, rank)),
                        kwargs=dict(scale_factor=1.7)),
            SampleInput(make_arg(shape(D, rank)),
                        kwargs=dict(scale_factor=0.6)),
        ])

    return sample_inputs
