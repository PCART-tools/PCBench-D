@pytest.mark.skipif(np.__version__ >= '1.13.0',
                    reason='boolean slicing rules changed')
def test_setitem_mixed_d():
    x = np.arange(24).reshape((4, 6))
    dx = da.from_array(x, chunks=(2, 2))

    x[x[0, None] > 2] = -1
    dx[dx[0, None] > 2] = -1
    assert_eq(x, dx)

    x[x[None, 0] > 2] = -1
    dx[dx[None, 0] > 2] = -1
    assert_eq(x, dx)
