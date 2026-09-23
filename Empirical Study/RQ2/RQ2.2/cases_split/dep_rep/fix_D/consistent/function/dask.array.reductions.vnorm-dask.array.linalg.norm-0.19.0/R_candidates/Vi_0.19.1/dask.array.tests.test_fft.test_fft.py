@pytest.mark.parametrize("funcname", all_1d_funcnames)
def test_fft(funcname):
    da_fft = getattr(da.fft, funcname)
    np_fft = getattr(np.fft, funcname)

    assert_eq(da_fft(darr),
              np_fft(nparr))
