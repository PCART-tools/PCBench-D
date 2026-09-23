def test_rfft_n_kwarg():
    assert eq(rfft(darr, 5), npfft.rfft(nparr, 5))
    assert eq(rfft(darr, 13), npfft.rfft(nparr, 13))
    assert eq(rfft(darr2, 5, axis=0), npfft.rfft(nparr, 5, axis=0))
    assert eq(rfft(darr2, 13, axis=0), npfft.rfft(nparr, 13, axis=0))
    assert eq(rfft(darr2, 12, axis=0), npfft.rfft(nparr, 12, axis=0))
