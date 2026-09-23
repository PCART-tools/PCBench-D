@pytest.mark.parametrize("shape, chunks, axis", [
    [(5,), (2,), None],
    [(5,), (2,), 0],
    [(5,), (2,), (0,)],
])
@pytest.mark.parametrize("norm", [
    0,
    2,
    -2,
    0.5,
])
@pytest.mark.parametrize("keepdims", [
    False,
    True,
])
def test_norm_1dim(shape, chunks, axis, norm, keepdims):
    a = np.random.random(shape)
    d = da.from_array(a, chunks=chunks)

    a_r = np.linalg.norm(a, ord=norm, axis=axis, keepdims=keepdims)
    d_r = da.linalg.norm(d, ord=norm, axis=axis, keepdims=keepdims)
    assert_eq(a_r, d_r)
