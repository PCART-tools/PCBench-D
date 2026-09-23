def test_DeferredVector_not_iterable():
    assert not iterable(DeferredVector('X'))
