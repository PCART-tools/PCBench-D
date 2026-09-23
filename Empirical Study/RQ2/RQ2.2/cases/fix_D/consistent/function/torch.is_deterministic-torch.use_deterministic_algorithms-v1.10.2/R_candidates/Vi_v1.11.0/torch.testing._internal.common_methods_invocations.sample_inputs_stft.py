def sample_inputs_stft(op_info, device, dtype, requires_grad, **kwargs):
    def mt(shape, **kwargs):
        return make_tensor(shape, device=device, dtype=dtype,
                           requires_grad=requires_grad, **kwargs)
    yield SampleInput(mt(100), kwargs=dict(n_fft=10))

    for center in [False, True]:
        yield SampleInput(mt(10), kwargs=dict(n_fft=7, center=center))
        yield SampleInput(mt((10, 100)), kwargs=dict(n_fft=16, hop_length=4, center=center))

    window = make_tensor(16, low=.5, high=2.0, dtype=dtype, device=device, requires_grad=requires_grad)
    yield SampleInput(
        mt((2, 100)), kwargs=dict(n_fft=16, window=window, return_complex=True, center=center))
    yield SampleInput(
        mt((3, 100)), kwargs=dict(n_fft=16, window=window, return_complex=True, center=center))
    if not dtype.is_complex:
        yield SampleInput(
            mt((10, 100)), kwargs=dict(n_fft=16, window=window, onesided=False))
