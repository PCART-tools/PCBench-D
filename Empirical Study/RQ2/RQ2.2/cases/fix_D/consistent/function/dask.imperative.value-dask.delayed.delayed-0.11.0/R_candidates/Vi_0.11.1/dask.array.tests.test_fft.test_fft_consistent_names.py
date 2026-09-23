def test_fft_consistent_names():
    assert same_keys(fft(darr, 5), fft(darr, 5))
    assert same_keys(fft(darr2, 5, axis=0), fft(darr2, 5, axis=0))
    assert not same_keys(fft(darr, 5), fft(darr, 13))
