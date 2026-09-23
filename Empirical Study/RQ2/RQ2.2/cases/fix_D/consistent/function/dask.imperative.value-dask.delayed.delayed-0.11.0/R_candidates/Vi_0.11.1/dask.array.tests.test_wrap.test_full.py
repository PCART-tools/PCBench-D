def test_full():
    a = da.full((3, 3), 100, chunks=(2, 2), dtype='i8')

    assert (a.compute() == 100).all()
    assert a._dtype == a.compute(get=dask.get).dtype == 'i8'
