def test_ihfft():
    assert_eq(ihfft(darr), npfft.ihfft(nparr))
    assert_eq(ihfft(darr2, axis=0), npfft.ihfft(nparr, axis=0))
