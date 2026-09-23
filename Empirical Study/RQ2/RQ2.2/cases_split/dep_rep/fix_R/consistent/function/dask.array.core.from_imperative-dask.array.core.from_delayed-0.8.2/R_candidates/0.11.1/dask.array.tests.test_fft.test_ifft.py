def test_ifft():
    assert_eq(ifft(darr), npfft.ifft(nparr))
    assert_eq(ifft(darr2, axis=0), npfft.ifft(nparr, axis=0))
