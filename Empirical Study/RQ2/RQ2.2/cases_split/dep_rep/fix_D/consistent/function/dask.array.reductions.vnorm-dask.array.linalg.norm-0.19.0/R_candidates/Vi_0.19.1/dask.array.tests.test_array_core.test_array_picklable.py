def test_array_picklable():
    from pickle import loads, dumps

    a = da.arange(100, chunks=25)
    a2 = loads(dumps(a))
    assert_eq(a, a2)
