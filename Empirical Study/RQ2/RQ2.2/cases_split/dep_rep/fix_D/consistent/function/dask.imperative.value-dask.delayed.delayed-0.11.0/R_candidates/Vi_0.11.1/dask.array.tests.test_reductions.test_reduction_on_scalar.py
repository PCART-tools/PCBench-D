def test_reduction_on_scalar():
    x = da.from_array(np.array(1.0), chunks=())
    assert (x == x).all()
