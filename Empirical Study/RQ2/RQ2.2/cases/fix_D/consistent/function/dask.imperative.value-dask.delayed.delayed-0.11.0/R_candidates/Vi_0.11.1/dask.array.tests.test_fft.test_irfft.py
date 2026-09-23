def test_irfft():
    assert_eq(irfft(darr), npfft.irfft(nparr))
    assert_eq(irfft(darr2, axis=0), npfft.irfft(nparr, axis=0))
