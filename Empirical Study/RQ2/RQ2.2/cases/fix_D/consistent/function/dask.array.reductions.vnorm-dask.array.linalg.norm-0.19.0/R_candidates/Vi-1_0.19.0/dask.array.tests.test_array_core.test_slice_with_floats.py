def test_slice_with_floats():
    d = da.ones((5,), chunks=(3,))
    with pytest.raises(IndexError):
        d[1.5]
    with pytest.raises(IndexError):
        d[0:1.5]
    with pytest.raises(IndexError):
        d[[1, 1.5]]
