@gen_cluster(client=True)
def test_persist(c, s, a, b):
    x = delayed(inc)(1)
    x2, = persist(x)

    yield _wait(x2)
    assert x2.key in a.data or x2.key in b.data

    y = delayed(inc)(10)
    y2, one = persist(y, 1)

    yield _wait(y2)
    assert y2.key in a.data or y2.key in b.data
