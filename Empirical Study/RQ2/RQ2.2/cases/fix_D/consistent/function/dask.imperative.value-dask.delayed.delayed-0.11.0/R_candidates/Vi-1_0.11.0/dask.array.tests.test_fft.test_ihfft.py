def test_ihfft():
    assert eq(ihfft(darr), npfft.ihfft(nparr))
    assert eq(ihfft(darr2, axis=0), npfft.ihfft(nparr, axis=0))
