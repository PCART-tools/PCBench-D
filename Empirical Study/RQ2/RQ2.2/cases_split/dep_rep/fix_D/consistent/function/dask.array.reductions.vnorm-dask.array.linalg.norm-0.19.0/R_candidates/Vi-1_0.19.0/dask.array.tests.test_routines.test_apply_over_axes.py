@pytest.mark.parametrize('func_name, func', [
    ["sum0", lambda x, axis: x.sum(axis=axis)],
    ["sum1", lambda x, axis: x.sum(axis=axis, keepdims=True)],
    [
        "range", lambda x, axis:
            np.concatenate(
                [
                    x.min(axis=axis, keepdims=True),
                    x.max(axis=axis, keepdims=True)
                ],
                axis=axis
            )
    ],
])
@pytest.mark.parametrize('shape, axes', [
    [(10, 15, 20), tuple()],
    [(10, 15, 20), 0],
    [(10, 15, 20), (1,)],
    [(10, 15, 20), (-1, 1)],
    [(10, 15, 20), (2, 0, 1)],
])
def test_apply_over_axes(func_name, func, shape, axes):
    a = np.random.randint(0, 10, shape)
    d = da.from_array(a, chunks=(len(shape) * (5,)))

    assert_eq(
        da.apply_over_axes(func, d, axes),
        np.apply_over_axes(func, a, axes)
    )
