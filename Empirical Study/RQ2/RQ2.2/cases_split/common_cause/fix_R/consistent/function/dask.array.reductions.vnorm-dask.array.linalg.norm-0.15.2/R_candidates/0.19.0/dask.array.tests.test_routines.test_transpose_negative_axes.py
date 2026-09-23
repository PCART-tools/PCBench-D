def test_transpose_negative_axes():
    x = np.ones((2, 3, 4, 5))
    y = da.ones((2, 3, 4, 5), chunks=3)

    assert_eq(x.transpose([-1, -2, 0, 1]),
              y.transpose([-1, -2, 0, 1]))
