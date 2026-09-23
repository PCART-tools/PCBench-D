def test_wrap_bad_kind():
    with pytest.raises(ValueError):
        fft_wrap(np.ones)
