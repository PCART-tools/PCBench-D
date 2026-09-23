@pytest.mark.parametrize('func1d_name, func1d', [
    ["ndim", lambda x: x.ndim],
    ["sum", lambda x: x.sum()],
    ["range", lambda x: [x.min(), x.max()]],
    ["range2", lambda x: [[x.min(), x.max()], [x.max(), x.min()]]],
])
@pytest.mark.parametrize('shape, axis', [
    [(10, 15, 20), 0],
    [(10, 15, 20), 1],
    [(10, 15, 20), 2],
    [(10, 15, 20), -1],
])
def test_apply_along_axis(func1d_name, func1d, shape, axis):
    a = np.random.randint(0, 10, shape)
    d = da.from_array(a, chunks=(len(shape) * (5,)))

    if (func1d_name == "range2" and
            LooseVersion(np.__version__) < LooseVersion("1.13.0")):
        with pytest.raises(ValueError):
            da.apply_along_axis(func1d, axis, d)
    else:
        assert_eq(
            da.apply_along_axis(func1d, axis, d),
            np.apply_along_axis(func1d, axis, a)
        )
