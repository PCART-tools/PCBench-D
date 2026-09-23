def test_irfft():
    assert eq(irfft(darr), npfft.irfft(nparr))
    assert eq(irfft(darr2, axis=0), npfft.irfft(nparr, axis=0))
