@pytest.mark.parametrize("funcname", all_1d_funcnames)
def test_cant_fft_chunked_axis(funcname):
    da_fft = getattr(da.fft, funcname)

    bad_darr = da.from_array(nparr, chunks=(5, 5))
    for i in range(bad_darr.ndim):
        with pytest.raises(ValueError):
            da_fft(bad_darr, axis=i)
