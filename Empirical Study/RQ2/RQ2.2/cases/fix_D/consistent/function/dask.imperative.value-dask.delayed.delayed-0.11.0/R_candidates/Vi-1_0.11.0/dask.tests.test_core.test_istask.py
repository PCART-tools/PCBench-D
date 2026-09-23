def test_istask():
    assert istask((inc, 1))
    assert not istask(1)
    assert not istask((1, 2))
    f = namedtuple('f', ['x', 'y'])
    assert not istask(f(sum, 2))
