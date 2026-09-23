def test_ifft():
    assert eq(ifft(darr), npfft.ifft(nparr))
    assert eq(ifft(darr2, axis=0), npfft.ifft(nparr, axis=0))
