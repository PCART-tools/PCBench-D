def test_lists():
    a = delayed(1)
    b = delayed(2)
    c = delayed(sum)([a, b])
    assert c.compute() == 3
