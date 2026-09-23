def test_fft_n_kwarg():
    assert_eq(fft(darr, 5), npfft.fft(nparr, 5))
    assert_eq(fft(darr, 13), npfft.fft(nparr, 13))
    assert_eq(fft(darr2, 5, axis=0), npfft.fft(nparr, 5, axis=0))
    assert_eq(fft(darr2, 13, axis=0), npfft.fft(nparr, 13, axis=0))
