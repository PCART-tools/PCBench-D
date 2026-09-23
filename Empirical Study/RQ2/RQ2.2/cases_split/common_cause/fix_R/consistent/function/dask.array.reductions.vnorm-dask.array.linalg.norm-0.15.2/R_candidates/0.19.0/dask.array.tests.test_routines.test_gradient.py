@pytest.mark.parametrize('shape, varargs, axis', [
    [(10, 15, 20), (), None],
    [(10, 15, 20), (2,), None],
    [(10, 15, 20), (1.0, 1.5, 2.0), None],
    [(10, 15, 20), (), 0],
    [(10, 15, 20), (), 1],
    [(10, 15, 20), (), 2],
    [(10, 15, 20), (), -1],
    [(10, 15, 20), (), (0, 2)],
])
@pytest.mark.parametrize('edge_order', [
    1,
    2
])
def test_gradient(shape, varargs, axis, edge_order):
    a = np.random.randint(0, 10, shape)
    d_a = da.from_array(a, chunks=(len(shape) * (5,)))

    r_a = np.gradient(a, *varargs, axis=axis, edge_order=edge_order)
    r_d_a = da.gradient(d_a, *varargs, axis=axis, edge_order=edge_order)

    if isinstance(axis, Number):
        assert_eq(r_d_a, r_a)
    else:
        assert len(r_d_a) == len(r_a)

        for e_r_d_a, e_r_a in zip(r_d_a, r_a):
            assert_eq(e_r_d_a, e_r_a)

        assert_eq(
            da.sqrt(sum(map(da.square, r_d_a))),
            np.sqrt(sum(map(np.square, r_a)))
        )
