@pytest.mark.parametrize("seed", [23, 796])
@pytest.mark.parametrize("low, high", [
    [0, 10]
])
@pytest.mark.parametrize("shape, chunks", [
    [(10,), (5,)],
    [(10,), (3,)],
    [(4, 5), (3, 2)],
    [(20, 20), (4, 5)],
])
def test_unique_rand(seed, low, high, shape, chunks):
    np.random.seed(seed)

    a = np.random.randint(low, high, size=shape)
    d = da.from_array(a, chunks=chunks)

    kwargs = dict(
        return_index=True,
        return_inverse=True,
        return_counts=True
    )

    r_a = np.unique(a, **kwargs)
    r_d = da.unique(d, **kwargs)

    assert len(r_a) == len(r_d)

    assert (d.size,) == r_d[2].shape

    for e_r_a, e_r_d in zip(r_a, r_d):
        assert_eq(e_r_d, e_r_a)
