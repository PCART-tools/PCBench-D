@pytest.mark.parametrize('shape, axis', [
    [(10, 15, 20), 0],
    [(10, 15, 20), 1],
    [(10, 15, 20), 2],
    [(10, 15, 20), -1],
])
@pytest.mark.parametrize('n', [
    0,
    1,
    2,
])
def test_diff(shape, n, axis):
    x = np.random.randint(0, 10, shape)
    a = da.from_array(x, chunks=(len(shape) * (5,)))

    assert_eq(da.diff(a, n, axis), np.diff(x, n, axis))
