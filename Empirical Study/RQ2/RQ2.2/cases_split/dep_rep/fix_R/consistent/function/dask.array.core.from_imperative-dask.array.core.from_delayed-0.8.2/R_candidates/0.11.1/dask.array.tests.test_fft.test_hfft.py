def test_hfft():
    assert_eq(hfft(darr), npfft.hfft(nparr))
    assert_eq(hfft(darr2, axis=0), npfft.hfft(nparr, axis=0))
