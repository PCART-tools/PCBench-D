@pytest.mark.parametrize("funcname", all_nd_funcnames)
def test_fft2n_shapes(funcname):
    da_fft = getattr(dask.array.fft, funcname)
    np_fft = getattr(np.fft, funcname)
    assert_eq(da_fft(darr3),
              np_fft(nparr))
    assert_eq(da_fft(darr3, (8, 9)),
              np_fft(nparr, (8, 9)))
    assert_eq(da_fft(darr3, (8, 9), axes=(1, 0)),
              np_fft(nparr, (8, 9), axes=(1, 0)))
    assert_eq(da_fft(darr3, (12, 11), axes=(1, 0)),
              np_fft(nparr, (12, 11), axes=(1, 0)))
