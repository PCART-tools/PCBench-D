def test_method_caller():
    a = [1, 2, 3, 3, 3]
    f = methodcaller('count')
    assert f(a, 3) == a.count(3)
    assert methodcaller('count') is f
    assert M.count is f
    assert pickle.loads(pickle.dumps(f)) is f
    assert 'count' in dir(M)
