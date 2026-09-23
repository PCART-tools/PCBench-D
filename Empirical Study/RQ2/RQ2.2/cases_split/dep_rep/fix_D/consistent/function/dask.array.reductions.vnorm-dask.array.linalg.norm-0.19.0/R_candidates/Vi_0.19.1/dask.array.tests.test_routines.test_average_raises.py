def test_average_raises():
    d_a = da.arange(11, chunks=2)

    with pytest.raises(TypeError):
        da.average(d_a, weights=[1, 2, 3])

    with pytest.warns(RuntimeWarning):
        da.average(d_a, weights=da.zeros_like(d_a)).compute()
