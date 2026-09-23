def test_ifft_n_kwarg():
    assert_eq(ifft(darr, 5), npfft.ifft(nparr, 5))
    assert_eq(ifft(darr, 13), npfft.ifft(nparr, 13))
    assert_eq(ifft(darr2, 5, axis=0), npfft.ifft(nparr, 5, axis=0))
    assert_eq(ifft(darr2, 13, axis=0), npfft.ifft(nparr, 13, axis=0))
