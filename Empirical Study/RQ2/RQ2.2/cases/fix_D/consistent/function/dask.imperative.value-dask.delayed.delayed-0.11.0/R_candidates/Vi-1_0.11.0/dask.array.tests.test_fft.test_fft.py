def test_fft():
    assert eq(fft(darr), npfft.fft(nparr))
    assert eq(fft(darr2, axis=0), npfft.fft(nparr, axis=0))
