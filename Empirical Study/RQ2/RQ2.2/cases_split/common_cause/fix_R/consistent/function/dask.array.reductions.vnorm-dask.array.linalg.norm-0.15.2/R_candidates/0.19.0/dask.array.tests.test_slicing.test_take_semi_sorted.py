def test_take_semi_sorted():
    x = da.ones(10, chunks=(5,))
    index = np.arange(15) % 10

    y = x[index]
    assert y.chunks == ((5, 5, 5),)
