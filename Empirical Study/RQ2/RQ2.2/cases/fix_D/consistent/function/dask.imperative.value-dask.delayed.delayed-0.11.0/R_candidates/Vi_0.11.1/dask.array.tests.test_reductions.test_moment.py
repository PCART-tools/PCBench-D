def test_moment():
    def moment(x, n, axis=None):
        return (((x - x.mean(axis=axis, keepdims=True)) ** n).sum(axis=axis) /
                np.ones_like(x).sum(axis=axis))

    # Poorly conditioned
    x = np.array([1., 2., 3.] * 10).reshape((3, 10)) + 1e8
    a = da.from_array(x, chunks=5)
    assert_eq(a.moment(2), moment(x, 2))
    assert_eq(a.moment(3), moment(x, 3))
    assert_eq(a.moment(4), moment(x, 4))

    x = np.arange(1, 122).reshape((11, 11)).astype('f8')
    a = da.from_array(x, chunks=(4, 4))
    assert_eq(a.moment(4, axis=1), moment(x, 4, axis=1))
    assert_eq(a.moment(4, axis=(1, 0)), moment(x, 4, axis=(1, 0)))

    # Tree reduction
    assert_eq(a.moment(order=4, split_every=4), moment(x, 4))
    assert_eq(a.moment(order=4, axis=0, split_every=4), moment(x, 4, axis=0))
    assert_eq(a.moment(order=4, axis=1, split_every=4), moment(x, 4, axis=1))
