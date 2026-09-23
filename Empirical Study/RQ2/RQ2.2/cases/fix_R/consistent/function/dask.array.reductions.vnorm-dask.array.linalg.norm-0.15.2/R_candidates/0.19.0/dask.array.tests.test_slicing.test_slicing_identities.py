def test_slicing_identities():
    a = da.ones((24, 16), chunks=((4, 8, 8, 4), (2, 6, 6, 2)))

    assert a is a[slice(None)]
    assert a is a[:]
    assert a is a[::]
    assert a is a[...]
    assert a is a[0:]
    assert a is a[0::]
    assert a is a[::1]
    assert a is a[0:len(a)]
    assert a is a[0::1]
    assert a is a[0:len(a):1]
