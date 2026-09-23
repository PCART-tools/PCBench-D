def test_rfft():
    assert eq(rfft(darr), npfft.rfft(nparr))
    assert eq(rfft(darr2, axis=0), npfft.rfft(nparr, axis=0))
