def test_flatiter():
    x = np.arange(5)
    it = x.flat
    assert 0 == next(it)
    assert 1 == next(it)
    ret = cbook.safe_first_element(it)
    assert ret == 0

    assert 0 == next(it)
    assert 1 == next(it)
