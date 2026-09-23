@pytest.mark.parametrize('shape, axis', [
    [(10, 15, 20), None],
    [(10, 15, 20), 0],
    [(10, 15, 20), 1],
    [(10, 15, 20), 2],
    [(10, 15, 20), -1],
])
def test_ptp(shape, axis):
    a = np.random.randint(0, 10, shape)
    d = da.from_array(a, chunks=(len(shape) * (5,)))

    assert_eq(da.ptp(d, axis), np.ptp(a, axis))
