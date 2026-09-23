def test_nout():
    func = delayed(lambda x: (x, -x), nout=2, pure=True)
    x = func(1)
    assert len(x) == 2
    a, b = x
    assert compute(a, b) == (1, -1)
    assert a._length is None
    assert b._length is None
    pytest.raises(TypeError, lambda: len(a))
    pytest.raises(TypeError, lambda: list(a))

    pytest.raises(ValueError, lambda: delayed(add, nout=-1))
    pytest.raises(ValueError, lambda: delayed(add, nout=True))

    func = delayed(add, nout=None)
    a = func(1)
    assert a._length is None
    pytest.raises(TypeError, lambda: list(a))
    pytest.raises(TypeError, lambda: len(a))

    func = delayed(lambda x: (x,), nout=1, pure=True)
    x = func(1)
    assert len(x) == 1
    a, = x
    assert a.compute() == 1
    assert a._length is None
    pytest.raises(TypeError, lambda: len(a))

    func = delayed(lambda x: tuple(), nout=0, pure=True)
    x = func(1)
    assert len(x) == 0
    assert x.compute() == tuple()
