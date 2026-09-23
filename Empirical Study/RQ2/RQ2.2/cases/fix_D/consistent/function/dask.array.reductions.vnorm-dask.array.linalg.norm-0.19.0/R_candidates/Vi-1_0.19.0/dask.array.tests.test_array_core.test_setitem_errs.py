def test_setitem_errs():
    x = da.ones((4, 4), chunks=(2, 2))

    with pytest.raises(ValueError):
        x[x > 1] = x
