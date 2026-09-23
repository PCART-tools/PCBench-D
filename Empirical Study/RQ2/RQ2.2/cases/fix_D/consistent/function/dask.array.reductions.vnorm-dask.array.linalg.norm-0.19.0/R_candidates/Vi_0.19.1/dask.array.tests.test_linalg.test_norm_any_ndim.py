@pytest.mark.parametrize("shape, chunks, axis", [
    [(5,), (2,), None],
    [(5,), (2,), 0],
    [(5,), (2,), (0,)],
    [(5, 6), (2, 2), None],
])
@pytest.mark.parametrize("norm", [
    None,
    1,
    -1,
    np.inf,
    -np.inf,
])
@pytest.mark.parametrize("keepdims", [
    False,
    True,
])
def test_norm_any_ndim(shape, chunks, axis, norm, keepdims):
    a = np.random.random(shape)
    d = da.from_array(a, chunks=chunks)

    a_r = np.linalg.norm(a, ord=norm, axis=axis, keepdims=keepdims)
    d_r = da.linalg.norm(d, ord=norm, axis=axis, keepdims=keepdims)

    assert_eq(a_r, d_r)
