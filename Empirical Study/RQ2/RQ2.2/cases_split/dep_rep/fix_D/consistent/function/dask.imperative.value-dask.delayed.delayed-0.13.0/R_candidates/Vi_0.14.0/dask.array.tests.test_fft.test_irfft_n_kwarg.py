def test_irfft_n_kwarg():
    assert_eq(irfft(darr, 5), npfft.irfft(nparr, 5))
    assert_eq(irfft(darr, 13), npfft.irfft(nparr, 13))
    assert_eq(irfft(darr2, 5, axis=0), npfft.irfft(nparr, 5, axis=0))
    assert_eq(irfft(darr2, 13, axis=0), npfft.irfft(nparr, 13, axis=0))
    assert_eq(irfft(darr2, 12, axis=0), npfft.irfft(nparr, 12, axis=0))
