def test_coarsen():
    x = np.random.randint(10, size=(24, 24))
    y = coarsen(np.sum, x, {0: 2, 1: 4})
    assert y.shape == (12, 6)
    assert y[0, 0] == np.sum(x[:2, :4])
