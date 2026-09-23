@pytest.mark.parametrize("seed", [23, 796])
@pytest.mark.parametrize("low, high", [
    [0, 10]
])
@pytest.mark.parametrize("elements_shape, elements_chunks", [
    [(10,), (5,)],
    [(10,), (3,)],
    [(4, 5), (3, 2)],
    [(20, 20), (4, 5)],
])
@pytest.mark.parametrize("test_shape, test_chunks", [
    [(10,), (5,)],
    [(10,), (3,)],
    [(4, 5), (3, 2)],
    [(20, 20), (4, 5)],
])
@pytest.mark.parametrize("invert", [True, False])
@pytest.mark.skipif(LooseVersion(np.__version__) < '1.13.0',
                    reason="np.isin is new in numpy 1.13")
def test_isin_rand(seed, low, high, elements_shape, elements_chunks,
                   test_shape, test_chunks, invert):
    rng = np.random.RandomState(seed)

    a1 = rng.randint(low, high, size=elements_shape)
    d1 = da.from_array(a1, chunks=elements_chunks)

    a2 = rng.randint(low, high, size=test_shape) - 5
    d2 = da.from_array(a2, chunks=test_chunks)

    with pytest.warns(None):
        r_a = np.isin(a1, a2, invert=invert)
        r_d = da.isin(d1, d2, invert=invert)
    assert_eq(r_a, r_d)
