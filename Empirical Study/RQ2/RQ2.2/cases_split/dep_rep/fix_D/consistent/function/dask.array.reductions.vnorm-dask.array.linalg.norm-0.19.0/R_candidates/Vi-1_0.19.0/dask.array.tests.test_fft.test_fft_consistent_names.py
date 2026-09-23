@pytest.mark.parametrize("funcname", all_1d_funcnames)
def test_fft_consistent_names(funcname):
    da_fft = getattr(da.fft, funcname)

    assert same_keys(da_fft(darr, 5), da_fft(darr, 5))
    assert same_keys(da_fft(darr2, 5, axis=0), da_fft(darr2, 5, axis=0))
    assert not same_keys(da_fft(darr, 5), da_fft(darr, 13))
