def test_delayed():
    add2 = delayed(add)
    assert add2(1, 2).compute() == 3
    assert (add2(1, 2) + 3).compute() == 6
    assert add2(add2(1, 2), 3).compute() == 6
    a = delayed(1)
    b = add2(add2(a, 2), 3)
    assert a.key in b.dask
