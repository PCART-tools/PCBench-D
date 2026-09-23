def test_equivalent():
    t1 = (add, 'a', 'b')
    t2 = (add, 'x', 'y')

    assert equivalent(t1, t1)
    assert not equivalent(t1, t2)
    assert equivalent(t1, t2, {'x': 'a', 'y': 'b'})
    assert not equivalent(t1, t2, {'a': 'x'})

    t1 = (add, (double, 'a'), (double, 'a'))
    t2 = (add, (double, 'b'), (double, 'c'))

    assert equivalent(t1, t1)
    assert not equivalent(t1, t2)
    assert equivalent(t1, t2, {'b': 'a', 'c': 'a'})
    assert not equivalent(t1, t2, {'b': 'a', 'c': 'd'})
    assert not equivalent(t2, t1, {'a': 'b'})

    # Test literal comparisons
    assert equivalent(1, 1)
    assert not equivalent(1, 2)
    assert equivalent((1, 2, 3), (1, 2, 3))
