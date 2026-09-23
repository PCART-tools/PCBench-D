def test_compute():
    a = delayed(1) + 5
    b = a + 1
    c = a + 2
    assert compute(b, c) == (7, 8)
    assert compute(b) == (7,)
    assert compute([a, b], c) == ([6, 7], 8)
