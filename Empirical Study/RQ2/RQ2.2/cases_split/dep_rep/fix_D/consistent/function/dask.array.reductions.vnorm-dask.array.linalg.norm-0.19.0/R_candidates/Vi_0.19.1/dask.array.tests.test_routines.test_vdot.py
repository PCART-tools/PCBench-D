@pytest.mark.parametrize('shape, chunks', [
    ((20,), (6,)),
    ((4, 5,), (2, 3)),
])
def test_vdot(shape, chunks):
    np.random.random(1337)

    x = 2 * np.random.random((2,) + shape) - 1
    x = x[0] + 1j * x[1]

    y = 2 * np.random.random((2,) + shape) - 1
    y = y[0] + 1j * y[1]

    a = da.from_array(x, chunks=chunks)
    b = da.from_array(y, chunks=chunks)

    assert_eq(np.vdot(x, y), da.vdot(a, b))
    assert_eq(np.vdot(y, x), da.vdot(b, a))
    assert_eq(da.vdot(a, b), da.vdot(b, a).conj())
