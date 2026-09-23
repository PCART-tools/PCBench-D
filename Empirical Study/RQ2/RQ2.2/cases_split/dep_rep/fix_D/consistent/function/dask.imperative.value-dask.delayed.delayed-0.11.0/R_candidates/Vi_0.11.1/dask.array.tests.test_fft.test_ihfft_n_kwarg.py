def test_ihfft_n_kwarg():
    assert_eq(ihfft(darr, 5), npfft.ihfft(nparr, 5))
    assert_eq(ihfft(darr, 13), npfft.ihfft(nparr, 13))
    assert_eq(ihfft(darr2, 5, axis=0), npfft.ihfft(nparr, 5, axis=0))
    assert_eq(ihfft(darr2, 13, axis=0), npfft.ihfft(nparr, 13, axis=0))
    assert_eq(ihfft(darr2, 12, axis=0), npfft.ihfft(nparr, 12, axis=0))
