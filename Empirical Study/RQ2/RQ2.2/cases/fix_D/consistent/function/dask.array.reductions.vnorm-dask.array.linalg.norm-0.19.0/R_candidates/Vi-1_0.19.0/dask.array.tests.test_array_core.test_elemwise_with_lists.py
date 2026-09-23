@pytest.mark.parametrize('chunks', (100, 6))
@pytest.mark.parametrize('other', [[0, 0, 1], [2, 1, 3], (0, 0, 1)])
def test_elemwise_with_lists(chunks, other):
    x = np.arange(12).reshape((4, 3))
    d = da.arange(12, chunks=chunks).reshape((4, 3))

    x2 = np.vstack([x[:, 0], x[:, 1], x[:, 2]]).T
    d2 = da.vstack([d[:, 0], d[:, 1], d[:, 2]]).T

    assert_eq(x2, d2)

    x3 = x2 * other
    d3 = d2 * other

    assert_eq(x3, d3)
