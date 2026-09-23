def test_traverse_false():
    # Create a list with a dask value, and test that it's not computed
    def fail(*args):
        raise ValueError("shouldn't have computed")

    a = delayed(fail)()

    # list
    x = [a, 1, 2, 3]
    res = delayed(x, traverse=False).compute()
    assert len(res) == 4
    assert res[0] is a
    assert res[1:] == x[1:]

    # tuple that looks like a task
    x = (fail, a, (fail, a))
    res = delayed(x, traverse=False).compute()
    assert isinstance(res, tuple)
    assert res[0] == fail
    assert res[1] is a

    # list containing task-like-things
    x = [1, (fail, a), a]
    res = delayed(x, traverse=False).compute()
    assert isinstance(res, list)
    assert res[0] == 1
    assert res[1][0] == fail and res[1][1] is a
    assert res[2] is a

    # traverse=False still hits top level
    b = delayed(1)
    x = delayed(b, traverse=False)
    assert x.compute() == 1
