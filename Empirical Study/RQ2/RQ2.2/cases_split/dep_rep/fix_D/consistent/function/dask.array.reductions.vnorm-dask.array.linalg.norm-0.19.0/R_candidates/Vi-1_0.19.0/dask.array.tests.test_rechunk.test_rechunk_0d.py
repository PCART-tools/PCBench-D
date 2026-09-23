def test_rechunk_0d():
    a = np.array(42)
    x = da.from_array(a, chunks=())
    y = x.rechunk(())
    assert y.chunks == ()
    assert y.compute() == a
