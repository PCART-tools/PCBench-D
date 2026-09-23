@pytest.mark.parametrize('shape1, shape2', [
    ((20,), (6,)),
    ((4, 5,), (2, 3)),
])
def test_inner(shape1, shape2):
    np.random.random(1337)

    x = 2 * np.random.random(shape1) - 1
    y = 2 * np.random.random(shape2) - 1

    a = da.from_array(x, chunks=3)
    b = da.from_array(y, chunks=3)

    assert_eq(np.outer(x, y), da.outer(a, b))
    assert_eq(np.outer(y, x), da.outer(b, a))
