@pytest.mark.parametrize('u_shape, v_shape', [
    [tuple(), (2, 3)],
    [(1,), (2, 3)],
    [(1, 1), (2, 3)],
    [(0, 3), (1, 3)],
    [(2, 0), (2, 1)],
    [(1, 0), (2, 1)],
    [(0, 1), (1, 3)],
])
def test_broadcast_operator(u_shape, v_shape):
    u = np.random.random(u_shape)
    v = np.random.random(v_shape)

    d_u = from_array(u, chunks=1)
    d_v = from_array(v, chunks=1)

    w = u * v
    d_w = d_u * d_v

    assert_eq(w, d_w)
