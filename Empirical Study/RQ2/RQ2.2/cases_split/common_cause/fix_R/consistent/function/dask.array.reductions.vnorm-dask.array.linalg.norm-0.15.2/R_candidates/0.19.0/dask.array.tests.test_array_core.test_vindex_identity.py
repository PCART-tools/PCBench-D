def test_vindex_identity():
    rng = da.random.RandomState(42)
    a, b = 10, 20

    x = rng.random(a, chunks=a // 2)
    assert x is x.vindex[:]
    assert x is x.vindex[:a]
    pytest.raises(IndexError, lambda: x.vindex[:a - 1])
    pytest.raises(IndexError, lambda: x.vindex[1:])
    pytest.raises(IndexError, lambda: x.vindex[0:a:2])

    x = rng.random((a, b), chunks=(a // 2, b // 2))
    assert x is x.vindex[:, :]
    assert x is x.vindex[:a, :b]
    pytest.raises(IndexError, lambda: x.vindex[:, :b - 1])
    pytest.raises(IndexError, lambda: x.vindex[:, 1:])
    pytest.raises(IndexError, lambda: x.vindex[:, 0:b:2])
