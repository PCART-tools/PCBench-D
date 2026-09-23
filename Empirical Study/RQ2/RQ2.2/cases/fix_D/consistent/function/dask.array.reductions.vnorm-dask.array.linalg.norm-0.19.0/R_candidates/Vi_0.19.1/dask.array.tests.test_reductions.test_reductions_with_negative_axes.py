def test_reductions_with_negative_axes():
    x = np.random.random((4, 4, 4))
    a = da.from_array(x, chunks=2)

    assert_eq(a.argmin(axis=-1), x.argmin(axis=-1))
    assert_eq(a.argmin(axis=-1, split_every=2), x.argmin(axis=-1))

    assert_eq(a.sum(axis=-1), x.sum(axis=-1))
    assert_eq(a.sum(axis=(0, -1)), x.sum(axis=(0, -1)))
