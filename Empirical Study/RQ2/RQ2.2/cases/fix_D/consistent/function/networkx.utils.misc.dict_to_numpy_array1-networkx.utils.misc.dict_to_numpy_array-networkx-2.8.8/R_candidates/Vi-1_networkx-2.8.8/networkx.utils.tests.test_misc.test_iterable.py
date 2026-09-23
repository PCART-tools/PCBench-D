def test_iterable():
    assert not iterable(None)
    assert not iterable(10)
    assert iterable([1, 2, 3])
    assert iterable((1, 2, 3))
    assert iterable({1: "A", 2: "X"})
    assert iterable("ABC")
