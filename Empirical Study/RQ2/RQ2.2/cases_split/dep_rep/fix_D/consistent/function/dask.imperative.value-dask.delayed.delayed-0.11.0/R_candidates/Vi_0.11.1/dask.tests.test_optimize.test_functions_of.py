def test_functions_of():
    a = lambda x: x
    b = lambda x: x
    assert functions_of((a, 1)) == set([a])
    assert functions_of((a, (b, 1))) == set([a, b])
    assert functions_of((a, [(b, 1)])) == set([a, b])
    assert functions_of((a, [[[(b, 1)]]])) == set([a, b])
    assert functions_of(1) == set()
    assert functions_of(a) == set()
    assert functions_of((a,)) == set([a])
