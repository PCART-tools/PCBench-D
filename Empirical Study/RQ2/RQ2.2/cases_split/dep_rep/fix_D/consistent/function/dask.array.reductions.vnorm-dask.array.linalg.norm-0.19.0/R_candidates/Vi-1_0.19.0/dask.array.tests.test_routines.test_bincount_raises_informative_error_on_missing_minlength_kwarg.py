def test_bincount_raises_informative_error_on_missing_minlength_kwarg():
    x = np.array([2, 1, 5, 2, 1])
    d = da.from_array(x, chunks=2)
    try:
        da.bincount(d)
    except Exception as e:
        assert 'minlength' in str(e)
    else:
        assert False
