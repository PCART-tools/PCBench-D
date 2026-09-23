def test_full():
    a = da.full((3, 3), 100, chunks=(2, 2), dtype='i8')

    assert (a.compute() == 100).all()
    assert a.dtype == a.compute(scheduler='sync').dtype == 'i8'

    assert a.name.startswith('full-')
