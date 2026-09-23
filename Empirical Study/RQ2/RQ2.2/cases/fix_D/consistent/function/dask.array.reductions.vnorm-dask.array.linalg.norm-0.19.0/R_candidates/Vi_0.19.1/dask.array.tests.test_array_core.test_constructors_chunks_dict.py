def test_constructors_chunks_dict():
    x = da.ones((20, 20), chunks={0: 10, 1: 5})
    assert x.chunks == ((10, 10), (5, 5, 5, 5))

    x = da.ones((20, 20), chunks={0: 10, 1: "auto"})
    assert x.chunks == ((10, 10), (20,))
