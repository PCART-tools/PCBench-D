def test_cant_fft_chunked_axis():
    bad_darr = da.from_array(nparr, chunks=(5, 5))
    assert raises(ValueError, lambda: fft(bad_darr))
    assert raises(ValueError, lambda: fft(bad_darr, axis=0))
