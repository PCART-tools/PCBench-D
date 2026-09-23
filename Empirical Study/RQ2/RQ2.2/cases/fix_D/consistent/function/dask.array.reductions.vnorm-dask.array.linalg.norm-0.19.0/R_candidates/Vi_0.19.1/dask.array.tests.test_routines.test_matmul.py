@pytest.mark.parametrize("x_shape, y_shape", [
    [(), ()],
    [(), (7,)],
    [(), (7, 11)],
    [(), (7, 11, 15)],
    [(), (7, 11, 15, 19)],
    [(7,), ()],
    [(7,), (7,)],
    [(11,), (11, 7)],
    [(15,), (7, 15, 11)],
    [(19,), (7, 11, 19, 15)],
    [(7, 11), ()],
    [(7, 11), (11,)],
    [(7, 11), (11, 7)],
    [(11, 15), (7, 15, 11)],
    [(15, 19), (7, 11, 19, 15)],
    [(7, 11, 15), ()],
    [(7, 11, 15), (15,)],
    [(7, 11, 15), (15, 7)],
    [(7, 11, 15), (7, 15, 11)],
    [(11, 15, 19), (7, 11, 19, 15)],
    [(7, 11, 15, 19), ()],
    [(7, 11, 15, 19), (19,)],
    [(7, 11, 15, 19), (19, 7)],
    [(7, 11, 15, 19), (11, 19, 13)],
    [(7, 11, 15, 19), (7, 11, 19, 15)],
])
def test_matmul(x_shape, y_shape):
    np.random.seed(3732)

    x = np.random.random(x_shape)[()]
    y = np.random.random(y_shape)[()]

    a = da.from_array(x, chunks=tuple((i // 2) for i in x.shape))
    b = da.from_array(y, chunks=tuple((i // 2) for i in y.shape))

    expected = None
    try:
        expected = np.matmul(x, y)
    except ValueError:
        pass

    for d1, d2 in itertools.product([a, x], [b, y]):
        if x.ndim == 0 or y.ndim == 0:
            with pytest.raises(ValueError):
                da.matmul(d1, d2)
        else:
            assert_eq(expected, da.matmul(d1, d2))
