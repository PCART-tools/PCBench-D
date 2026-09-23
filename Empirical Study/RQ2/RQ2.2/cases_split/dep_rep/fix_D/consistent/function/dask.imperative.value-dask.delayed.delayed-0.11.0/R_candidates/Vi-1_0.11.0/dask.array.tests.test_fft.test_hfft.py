def test_hfft():
    assert eq(hfft(darr), npfft.hfft(nparr))
    assert eq(hfft(darr2, axis=0), npfft.hfft(nparr, axis=0))
