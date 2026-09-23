def test_hfft_nkwarg():
    assert eq(hfft(darr, 5), npfft.hfft(nparr, 5))
    assert eq(hfft(darr, 13), npfft.hfft(nparr, 13))
    assert eq(hfft(darr2, 5, axis=0), npfft.hfft(nparr, 5, axis=0))
    assert eq(hfft(darr2, 13, axis=0), npfft.hfft(nparr, 13, axis=0))
    assert eq(hfft(darr2, 12, axis=0), npfft.hfft(nparr, 12, axis=0))
