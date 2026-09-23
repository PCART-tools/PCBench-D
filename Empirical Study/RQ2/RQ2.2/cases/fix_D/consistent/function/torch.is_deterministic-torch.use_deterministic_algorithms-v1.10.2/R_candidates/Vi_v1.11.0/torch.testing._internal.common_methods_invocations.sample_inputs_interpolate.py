def sample_inputs_interpolate(mode, self, device, dtype, requires_grad, **kwargs):
    N, C = 2, 3
    D = 4
    S = 3
    L = 5

    align_corners_options: Tuple[Any, ...] = (None,)
    if mode in ('linear', 'bilinear', 'bicubic', 'trilinear'):
        align_corners_options = (True, False, None)
    ranks_for_mode = {
        'nearest': [1, 2, 3],
        'linear': [1],
        'bilinear': [2],
        'bicubic': [2],
        'trilinear': [3],
        'area': [1, 2, 3]
    }

    def shape(size, rank, with_batch_channel=True):
        if with_batch_channel:
            return tuple([N, C] + ([size] * rank))
        return tuple([size] * rank)

    make_arg = partial(make_tensor, device=device, dtype=dtype,
                       requires_grad=requires_grad, low=-1, high=1)

    sample_inputs = []
    for align_corners in align_corners_options:
        for rank in ranks_for_mode[mode]:
            sample_inputs.extend([
                SampleInput(make_arg(shape(D, rank)),
                            args=(shape(S, rank, False), None, mode, align_corners)),
                SampleInput(make_arg(shape(D, rank)),
                            args=(shape(L, rank, False), None, mode, align_corners)),
                SampleInput(make_arg(shape(D, rank)),
                            args=(None, 1.7, mode, align_corners)),
                SampleInput(make_arg(shape(D, rank)),
                            args=(None, 0.6, mode, align_corners)),
            ])

    return sample_inputs
