def test_A_property():
    x = da.ones(5, chunks=(2,))
    assert x.A is x
