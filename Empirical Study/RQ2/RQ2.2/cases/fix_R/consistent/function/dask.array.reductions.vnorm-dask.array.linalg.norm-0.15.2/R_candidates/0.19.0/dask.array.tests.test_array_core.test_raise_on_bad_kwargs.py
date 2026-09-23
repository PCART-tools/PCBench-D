def test_raise_on_bad_kwargs():
    x = da.ones(5, chunks=3)
    try:
        da.minimum(x, foo=None)
    except TypeError as e:
        assert 'minimum' in str(e)
        assert 'foo' in str(e)
