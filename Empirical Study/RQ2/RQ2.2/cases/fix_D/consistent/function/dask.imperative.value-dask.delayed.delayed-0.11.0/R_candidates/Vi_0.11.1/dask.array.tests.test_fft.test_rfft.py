def test_rfft():
    assert_eq(rfft(darr), npfft.rfft(nparr))
    assert_eq(rfft(darr2, axis=0), npfft.rfft(nparr, axis=0))
