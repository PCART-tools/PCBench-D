@pytest.mark.parametrize("funcname", all_1d_funcnames)
def test_fft_n_kwarg(funcname):
    da_fft = getattr(da.fft, funcname)
    np_fft = getattr(np.fft, funcname)

    assert_eq(da_fft(darr, 5),
              np_fft(nparr, 5))
    assert_eq(da_fft(darr, 13),
              np_fft(nparr, 13))
    assert_eq(da_fft(darr2, axis=0),
              np_fft(nparr, axis=0))
    assert_eq(da_fft(darr2, 5, axis=0),
              np_fft(nparr, 5, axis=0))
    assert_eq(da_fft(darr2, 13, axis=0),
              np_fft(nparr, 13, axis=0))
    assert_eq(da_fft(darr2, 12, axis=0),
              np_fft(nparr, 12, axis=0))
