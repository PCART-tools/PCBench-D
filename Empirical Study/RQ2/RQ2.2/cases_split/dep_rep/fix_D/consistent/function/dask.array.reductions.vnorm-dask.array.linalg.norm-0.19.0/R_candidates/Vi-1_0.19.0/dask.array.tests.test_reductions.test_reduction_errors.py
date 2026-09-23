def test_reduction_errors():
    x = da.ones((5, 5), chunks=(3, 3))
    with pytest.raises(ValueError):
        x.sum(axis=2)
    with pytest.raises(ValueError):
        x.sum(axis=-3)
