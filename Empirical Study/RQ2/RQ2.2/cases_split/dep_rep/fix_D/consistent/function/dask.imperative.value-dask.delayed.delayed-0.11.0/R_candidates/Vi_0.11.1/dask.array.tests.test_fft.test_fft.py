def test_fft():
    assert_eq(fft(darr), npfft.fft(nparr))
    assert_eq(fft(darr2, axis=0), npfft.fft(nparr, axis=0))
